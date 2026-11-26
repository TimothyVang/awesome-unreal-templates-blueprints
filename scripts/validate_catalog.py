#!/usr/bin/env python3
"""Validate Markdown structure, anchors, generated filter views, URL hygiene, and optional live GitHub status."""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import subprocess
import sys
import time
from urllib.parse import urlsplit

ROOT = pathlib.Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
UNREAL_NOTES = ROOT / "catalogs" / "UNREAL.md"
GENERATED_MD = (
    ROOT / "catalogs" / "UE58_READY.md",
    ROOT / "catalogs" / "MIT_APACHE_COMMERCIAL_SAFE.md",
    ROOT / "catalogs" / "BLUEPRINT_ONLY.md",
)
INDEX_JSON = ROOT / "catalogs" / "INDEX.json"

MD_LINK_RE = re.compile(r"(?<!!)\[([^\]]+)\]\(([^)\s]+)\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
PUBLIC_RISK_RE = re.compile(
    r"(?i)(?:[a-z]:[\\/](?:users|windows)[\\/]|"
    r"(?:github_pat_|gh[pousr]_)\w+|"
    r"x-amz-(?:signature|credential)=|"
    r"https?://(?:localhost|127\.0\.0\.1|10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+))"
)


def gh_slug(heading_text: str) -> str:
    s = heading_text.lower().strip()
    out = [ch for ch in s if ch.isalnum() or ch in (" ", "-")]
    return re.sub(r" ", "-", "".join(out))


def parse_table_blocks(lines: list[str]) -> list[tuple[int, list[str]]]:
    blocks: list[tuple[int, list[str]]] = []
    cur_start = 0
    cur: list[str] = []
    in_fence = False
    for idx, line in enumerate(lines, 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
        if not in_fence and stripped.startswith("|") and stripped.endswith("|"):
            if not cur:
                cur_start = idx
            cur.append(stripped)
        else:
            if cur:
                blocks.append((cur_start, cur))
                cur = []
    if cur:
        blocks.append((cur_start, cur))
    return blocks


def validate_tables(path: pathlib.Path, lines: list[str], errors: list[str]) -> None:
    rel = path.relative_to(ROOT).as_posix()
    for start_line, rows in parse_table_blocks(lines):
        if len(rows) < 3:
            errors.append(f"{rel}:{start_line}: table has fewer than 3 rows")
            continue
        header_cols = len(rows[0].strip("|").split("|"))
        for offset, row in enumerate(rows):
            cells = [c.strip() for c in row.strip("|").split("|")]
            if len(cells) != header_cols:
                errors.append(
                    f"{rel}:{start_line + offset}: expected {header_cols} columns, got {len(cells)}"
                )
            if offset != 1 and any(c == "" for c in cells):
                errors.append(f"{rel}:{start_line + offset}: empty table cell")


def validate_markdown_links(path: pathlib.Path, text: str, slugs: set[str], errors: list[str], enforce_sec_dedup: bool) -> set[str]:
    rel = path.relative_to(ROOT).as_posix()
    current_section = "header"
    sec_urls: dict[str, set[str]] = {current_section: set()}
    all_urls: set[str] = set()
    in_fence = False

    for lineno, line in enumerate(text.splitlines(), 1):
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if line.startswith("## "):
            current_section = line.strip()
            sec_urls.setdefault(current_section, set())

        for label, target in MD_LINK_RE.findall(line):
            if target.startswith("#"):
                anchor = target[1:]
                if anchor not in slugs:
                    errors.append(f"{rel}:{lineno}: broken anchor ({target}) on [{label}]")
            elif target.startswith(("http://", "https://")):
                sp = urlsplit(target)
                if sp.scheme != "https":
                    errors.append(f"{rel}:{lineno}: non-HTTPS link {target}")
                norm = target.rstrip("/").lower()
                all_urls.add(norm)
                if enforce_sec_dedup and current_section.startswith("## ") and re.match(r"^## \d+\.", current_section):
                    if norm in sec_urls[current_section]:
                        errors.append(f"{rel}:{lineno}: duplicate URL in {current_section}: {target}")
                    sec_urls[current_section].add(norm)
            else:
                rel_target = (path.parent / target.split("#")[0]).resolve()
                if not rel_target.exists():
                    errors.append(f"{rel}:{lineno}: missing relative file target {target}")

    return all_urls


def validate_readme(text: str, errors: list[str]) -> set[str]:
    lines = text.splitlines()
    if PUBLIC_RISK_RE.search(text):
        errors.append("README.md: contains private path, token, or localhost URL")

    validate_tables(README, lines, errors)

    slugs: set[str] = set()
    numbered_sections: list[int] = []
    in_fence = False
    for line in lines:
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADING_RE.match(line)
        if m:
            title = m.group(2)
            slugs.add(gh_slug(title))
            sm = re.match(r"^(\d+)\.\s+", title)
            if m.group(1) == "##" and sm:
                numbered_sections.append(int(sm.group(1)))

    expected_nums = list(range(1, len(numbered_sections) + 1))
    if numbered_sections != expected_nums or len(numbered_sections) < 40:
        errors.append(f"README.md: expected >= 40 sequential sections, got {numbered_sections}")

    return validate_markdown_links(README, text, slugs, errors, enforce_sec_dedup=True)


def validate_unreal_notes(text: str, errors: list[str]) -> set[str]:
    lines = text.splitlines()
    if PUBLIC_RISK_RE.search(text):
        errors.append("catalogs/UNREAL.md: contains private path, token, or localhost URL")
    validate_tables(UNREAL_NOTES, lines, errors)
    if text.count("](../README.md)") < 1:
        errors.append("catalogs/UNREAL.md: missing back-link to ../README.md")

    loop_rows = [l for l in lines if re.match(r"^\|\s*\d{2}\s*\|", l)]
    if len(loop_rows) < 60:
        errors.append(f"catalogs/UNREAL.md: expected >= 60 loop rows, got {len(loop_rows)}")

    urls: set[str] = set()
    names: set[str] = set()
    for idx, line in enumerate(loop_rows, 1):
        fields = [f.strip() for f in line.strip("|").split("|")]
        if fields[0] != f"{idx:02d}":
            errors.append(f"catalogs/UNREAL.md: loop sequence mismatch at {idx}: got {fields[0]}")
        if "**" in fields[1]:
            use_case = fields[1].split("**")[1].casefold()
            if use_case in names:
                errors.append(f"catalogs/UNREAL.md: duplicate use case '{use_case}'")
            names.add(use_case)
        links = [t for _, t in MD_LINK_RE.findall(line)]
        if not links or any(urlsplit(u).scheme != "https" for u in links):
            errors.append(f"catalogs/UNREAL.md: invalid HTTPS link on loop {idx:02d}")
        for u in links:
            urls.add(u.rstrip("/").lower())
    return urls


def validate_generated_indexes(errors: list[str]) -> None:
    proc = subprocess.run(
        [sys.executable, "-B", str(ROOT / "scripts" / "build_indexes.py"), "--check"],
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if proc.returncode != 0:
        errors.append(f"Generated filter catalogs out of sync: {proc.stderr.strip() or proc.stdout.strip()}")
        return

    for md_path in GENERATED_MD:
        txt = md_path.read_text(encoding="utf-8")
        if PUBLIC_RISK_RE.search(txt):
            errors.append(f"{md_path.name}: contains private path, token, or localhost URL")
        validate_tables(md_path, txt.splitlines(), errors)
        slugs = {
            gh_slug(m.group(2))
            for l in txt.splitlines()
            if (m := HEADING_RE.match(l))
        }
        validate_markdown_links(md_path, txt, slugs, errors, enforce_sec_dedup=False)

    if not INDEX_JSON.exists():
        errors.append("Missing catalogs/INDEX.json")
    else:
        data = json.loads(INDEX_JSON.read_text(encoding="utf-8"))
        if data.get("stats", {}).get("sections", 0) < 38 or len(data.get("entries", [])) < 400:
            errors.append(f"catalogs/INDEX.json stats unexpectedly small: {data.get('stats')}")


def verify_github_live(errors: list[str]) -> int:
    repo_occurrences: dict[tuple[str, str], list[tuple[str, int, str, str]]] = {}
    for rel in (README, UNREAL_NOTES):
        txt = rel.read_text(encoding="utf-8")
        for lineno, line in enumerate(txt.splitlines(), 1):
            for label, target in MD_LINK_RE.findall(line):
                sp = urlsplit(target)
                if sp.netloc.lower() == "github.com":
                    parts = [p for p in sp.path.strip("/").split("/") if p]
                    if len(parts) >= 2 and parts[0].lower() not in ("topics", "orgs", "users"):
                        if len(parts) >= 4 and parts[2] == "actions":
                            continue
                        owner, name = parts[0], parts[1].removesuffix(".git")
                        key = (owner.lower(), name.lower())
                        repo_occurrences.setdefault(key, []).append(
                            (rel.name, lineno, label, line)
                        )

    items = [(k, v[0][3], k[0], k[1]) for k, v in repo_occurrences.items()]
    batch_size = 40
    checked = 0
    for i in range(0, len(items), batch_size):
        if i > 0:
            time.sleep(0.4)
        chunk = items[i : i + batch_size]
        q = ["query {"]
        for idx, (key, _, owner, name) in enumerate(chunk):
            q.append(
                f'r{idx}: repository(owner: {json.dumps(owner)}, name: {json.dumps(name)}) {{ '
                f'nameWithOwner isArchived isDisabled isEmpty }}'
            )
        q.append("}")
        proc = None
        for attempt in range(6):
            proc = subprocess.run(
                ["gh", "api", "graphql", "-f", "query=" + " ".join(q)],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            if proc.returncode == 0 or proc.stdout.strip().startswith("{"):
                break
            time.sleep(2.0 * (attempt + 1))
        if proc is None or (proc.returncode != 0 and not proc.stdout.strip().startswith("{")):
            errors.append(f"GitHub GraphQL call failed: {(proc.stderr if proc else '')[:200]}")
            break
        data = (json.loads(proc.stdout).get("data") or {})
        for idx, (key, _, owner, name) in enumerate(chunk):
            node = data.get(f"r{idx}")
            if not node:
                rp = subprocess.run(
                    ["gh", "api", f"repos/{owner}/{name}"],
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                )
                if rp.returncode != 0:
                    locs = ", ".join(f"{f}:{ln}" for f, ln, _, _ in repo_occurrences[key])
                    errors.append(f"Dead GitHub repo {owner}/{name} at {locs}")
                    continue
                rj = json.loads(rp.stdout)
                node = {
                    "nameWithOwner": rj["full_name"],
                    "isArchived": rj["archived"],
                    "isDisabled": rj.get("disabled", False),
                    "isEmpty": rj.get("size", 1) == 0,
                }
            checked += 1
            if node.get("isDisabled") or node.get("isEmpty"):
                locs = ", ".join(f"{f}:{ln}" for f, ln, _, _ in repo_occurrences[key])
                errors.append(f"Disabled/empty GitHub repo {node['nameWithOwner']} at {locs}")
            if node.get("isArchived"):
                for fname, ln, lbl, full_line in repo_occurrences[key]:
                    if fname == "README.md" and "archived" not in full_line.lower():
                        errors.append(
                            f"{fname}:{ln}: repo {node['nameWithOwner']} is archived on GitHub "
                            f"but not marked (Archived) on its row"
                        )
    return checked


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-github", action="store_true", help="Verify all GitHub repos via gh CLI")
    args = parser.parse_args()

    errors: list[str] = []
    if not README.exists():
        errors.append("Missing README.md")
    if not UNREAL_NOTES.exists():
        errors.append("Missing catalogs/UNREAL.md")

    readme_text = README.read_text(encoding="utf-8")
    notes_text = UNREAL_NOTES.read_text(encoding="utf-8")

    for req_link in (
        "catalogs/UNREAL.md",
        "catalogs/UE58_READY.md",
        "catalogs/MIT_APACHE_COMMERCIAL_SAFE.md",
        "catalogs/BLUEPRINT_ONLY.md",
        "catalogs/INDEX.json",
    ):
        if f"]({req_link})" not in readme_text:
            errors.append(f"README.md: missing link to {req_link}")

    r_urls = validate_readme(readme_text, errors)
    u_urls = validate_unreal_notes(notes_text, errors)
    validate_generated_indexes(errors)
    combined = r_urls | u_urls
    if len(combined) < 1180:
        errors.append(f"Expected >= 1180 unique verified HTTPS links matching badge claim, got {len(combined)}")

    gh_checked = 0
    if args.verify_github:
        gh_checked = verify_github_live(errors)

    if errors:
        print(f"VALIDATION FAILED with {len(errors)} error(s):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    msg = (
        f"OK: README.md ({len(r_urls)} unique HTTPS links) + "
        f"catalogs/UNREAL.md ({len(u_urls)} unique HTTPS links) = "
        f"{len(combined)} unique links + 4 generated filter/JSON views validated cleanly."
    )
    if args.verify_github:
        msg += f" Live GitHub API verified {gh_checked} unique repositories."
    print(msg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
