#!/usr/bin/env python3
"""Validate Markdown structure, anchors, SPDX-verified filter views, URL hygiene, and optional live GitHub status."""

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
GITHUB_SPDX_PATH = ROOT / "catalogs" / "GITHUB_SPDX.json"
GENERATED_MD = (
    ROOT / "catalogs" / "UE58_READY.md",
    ROOT / "catalogs" / "MIT_APACHE_COMMERCIAL_SAFE.md",
    ROOT / "catalogs" / "BLUEPRINT_ONLY.md",
)
INDEX_JSON = ROOT / "catalogs" / "INDEX.json"

PERMISSIVE_SPDX = frozenset({
    "MIT",
    "Apache-2.0",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "0BSD",
    "ISC",
    "CC0-1.0",
    "Unlicense",
    "Zlib",
    "BSL-1.0",
})

IMAGE_MD_RE = re.compile(r"!\[[^\]]*\]\([^)\s]+\)")
MD_LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)\s]+)\)")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
DELIMITER_CELL_RE = re.compile(r"^:?-{3,}:?$")
PUBLIC_RISK_RE = re.compile(
    r"(?i)(?:[a-z]:[\\/](?:users|windows)[\\/]|"
    r"/(?:users|home)/[a-z0-9_.-]+/|"
    r"(?:github_pat_|gh[pousr]_)\w+|"
    r"x-amz-(?:signature|credential)=|"
    r"https?://(?:localhost|127\.0\.0\.1|10\.\d+\.\d+\.\d+|192\.168\.\d+\.\d+))"
)


def strip_images(line: str) -> str:
    return IMAGE_MD_RE.sub("BADGE_IMG", line)


def gh_slug(heading_text: str) -> str:
    cleaned = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", heading_text)
    cleaned = re.sub(r"[`*~]", "", cleaned).lower().strip()
    out = [ch for ch in cleaned if ch.isalnum() or ch in (" ", "-", "_")]
    return re.sub(r" ", "-", "".join(out))


def collect_slugs(text: str) -> set[str]:
    slugs: set[str] = set()
    counts: dict[str, int] = {}
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADING_RE.match(line)
        if m:
            base = gh_slug(m.group(2))
            idx = counts.get(base, 0)
            slugs.add(base if idx == 0 else f"{base}-{idx}")
            counts[base] = idx + 1
    return slugs


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
            if offset == 1:
                if not all(DELIMITER_CELL_RE.match(c) for c in cells):
                    errors.append(f"{rel}:{start_line + 1}: missing or invalid Markdown table delimiter row")
            elif any(c == "" for c in cells):
                errors.append(f"{rel}:{start_line + offset}: empty table cell")


def validate_markdown_links(
    path: pathlib.Path,
    text: str,
    slugs: set[str],
    errors: list[str],
    enforce_sec_dedup: bool,
) -> set[str]:
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

        clean_line = strip_images(line)
        for label, target in MD_LINK_RE.findall(clean_line):
            if target.startswith("#"):
                anchor = target[1:]
                if anchor not in slugs:
                    errors.append(f"{rel}:{lineno}: broken anchor ({target}) on [{label}]")
            elif target.startswith(("http://", "https://")):
                sp = urlsplit(target)
                if sp.scheme != "https":
                    errors.append(f"{rel}:{lineno}: non-HTTPS link {target}")
                if sp.path.endswith("/badge.svg") or "/actions/workflows/" in sp.path or target == "https://awesome.re":
                    continue
                norm = target.rstrip("/").lower()
                all_urls.add(norm)
                if enforce_sec_dedup and current_section.startswith("## ") and re.match(r"^## \d+\.", current_section):
                    if norm in sec_urls[current_section]:
                        errors.append(f"{rel}:{lineno}: duplicate URL in {current_section}: {target}")
                    sec_urls[current_section].add(norm)
            else:
                file_part, _, frag = target.partition("#")
                rel_target = (path.parent / file_part).resolve()
                if not rel_target.exists():
                    errors.append(f"{rel}:{lineno}: missing relative file target {target}")
                elif frag and rel_target.suffix.lower() == ".md":
                    target_slugs = collect_slugs(rel_target.read_text(encoding="utf-8"))
                    if frag not in target_slugs:
                        errors.append(f"{rel}:{lineno}: broken cross-file anchor ({target})")

    return all_urls


def validate_readme(text: str, errors: list[str]) -> set[str]:
    lines = text.splitlines()
    validate_tables(README, lines, errors)

    slugs = collect_slugs(text)
    numbered_sections: list[int] = []
    in_fence = False
    for line in lines:
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADING_RE.match(line)
        if m and m.group(1) == "##":
            sm = re.match(r"^(\d+)\.\s+", m.group(2))
            if sm:
                numbered_sections.append(int(sm.group(1)))

    expected_nums = list(range(1, len(numbered_sections) + 1))
    if numbered_sections != expected_nums or len(numbered_sections) < 40:
        errors.append(f"README.md: expected >= 40 sequential sections, got {numbered_sections}")

    return validate_markdown_links(README, text, slugs, errors, enforce_sec_dedup=True)


def validate_unreal_notes(text: str, errors: list[str]) -> set[str]:
    lines = text.splitlines()
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
        links = [t for _, t in MD_LINK_RE.findall(strip_images(line))]
        if not links or any(urlsplit(u).scheme != "https" for u in links):
            errors.append(f"catalogs/UNREAL.md: invalid HTTPS link on loop {idx:02d}")
        for u in links:
            urls.add(u.rstrip("/").lower())
    return urls


def validate_public_hygiene(errors: list[str]) -> None:
    candidates = [
        README,
        UNREAL_NOTES,
        ROOT / "CONTRIBUTING.md",
        ROOT / ".deepmodebot.json",
        GITHUB_SPDX_PATH,
        INDEX_JSON,
        *GENERATED_MD,
        *(ROOT / ".github" / "workflows").glob("*.yml"),
        *(ROOT / "scripts").glob("*.py"),
    ]
    this_file = pathlib.Path(__file__).resolve()
    for p in candidates:
        if not p.exists() or p.resolve() == this_file:
            continue
        txt = p.read_text(encoding="utf-8")
        if PUBLIC_RISK_RE.search(txt):
            errors.append(f"{p.relative_to(ROOT).as_posix()}: contains private path, token, or localhost URL")


def validate_generated_indexes(spdx_db: dict[str, dict[str, object]], errors: list[str]) -> None:
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
        validate_tables(md_path, txt.splitlines(), errors)
        slugs = collect_slugs(txt)
        validate_markdown_links(md_path, txt, slugs, errors, enforce_sec_dedup=True)

    # Strict semantic audit on MIT_APACHE_COMMERCIAL_SAFE.md against GITHUB_SPDX.json
    safe_txt = (ROOT / "catalogs" / "MIT_APACHE_COMMERCIAL_SAFE.md").read_text(encoding="utf-8")
    for lineno, line in enumerate(safe_txt.splitlines(), 1):
        for _, target in MD_LINK_RE.findall(strip_images(line)):
            sp = urlsplit(target)
            if sp.netloc.lower() == "github.com":
                parts = [p for p in sp.path.strip("/").split("/") if p]
                if len(parts) >= 2:
                    key = f"{parts[0].lower()}/{parts[1].lower().removesuffix('.git')}"
                    info = spdx_db.get(key)
                    if not info or info.get("spdx") not in PERMISSIVE_SPDX or info.get("archived"):
                        errors.append(
                            f"MIT_APACHE_COMMERCIAL_SAFE.md:{lineno}: non-permissive or archived repo {key} ({info})"
                        )

    # Strict semantic audit on BLUEPRINT_ONLY.md
    bp_txt = (ROOT / "catalogs" / "BLUEPRINT_ONLY.md").read_text(encoding="utf-8")
    for lineno, line in enumerate(bp_txt.splitlines(), 1):
        if line.startswith("## "):
            m = re.match(r"^## (\d+)\.", line)
            if m and int(m.group(1)) > 21:
                errors.append(f"BLUEPRINT_ONLY.md:{lineno}: unexpected non-gameplay section {line}")
        elif line.startswith("| **"):
            low = line.lower()
            if "c++" in low and "no c++" not in low and "zero c++" not in low:
                errors.append(f"BLUEPRINT_ONLY.md:{lineno}: C++ hybrid leaked into pure-Blueprint view")

    if not INDEX_JSON.exists():
        errors.append("Missing catalogs/INDEX.json")
    else:
        data = json.loads(INDEX_JSON.read_text(encoding="utf-8"))
        if data.get("stats", {}).get("tableBackedSections", 0) < 38 or len(data.get("entries", [])) < 400:
            errors.append(f"catalogs/INDEX.json stats unexpectedly small: {data.get('stats')}")


def verify_github_live(spdx_db: dict[str, dict[str, object]], errors: list[str]) -> int:
    repo_occurrences: dict[str, list[tuple[str, int, str, str]]] = {}
    for rel in (README, UNREAL_NOTES):
        txt = rel.read_text(encoding="utf-8")
        for lineno, line in enumerate(txt.splitlines(), 1):
            for label, target in MD_LINK_RE.findall(strip_images(line)):
                sp = urlsplit(target)
                if sp.netloc.lower() == "github.com":
                    parts = [p for p in sp.path.strip("/").split("/") if p]
                    if len(parts) >= 2 and parts[0].lower() not in ("topics", "orgs", "users"):
                        if len(parts) >= 4 and parts[2] == "actions":
                            continue
                        owner, name = parts[0], parts[1].removesuffix(".git")
                        key = f"{owner.lower()}/{name.lower()}"
                        repo_occurrences.setdefault(key, []).append(
                            (rel.name, lineno, label, line)
                        )

    items = [(k, k.split("/", 1)[0], k.split("/", 1)[1]) for k in sorted(repo_occurrences)]
    batch_size = 40
    checked = 0
    live_spdx: dict[str, tuple[str, bool]] = {}

    for i in range(0, len(items), batch_size):
        if i > 0:
            time.sleep(0.4)
        chunk = items[i : i + batch_size]
        q = ["query {"]
        for idx, (key, owner, name) in enumerate(chunk):
            q.append(
                f'r{idx}: repository(owner: {json.dumps(owner)}, name: {json.dumps(name)}) {{ '
                f'nameWithOwner isArchived isDisabled isEmpty licenseInfo {{ spdxId }} }}'
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
        for idx, (key, owner, name) in enumerate(chunk):
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
                    "licenseInfo": {"spdxId": (rj.get("license") or {}).get("spdx_id")},
                }
            checked += 1
            spdx_id = (node.get("licenseInfo") or {}).get("spdxId") or "NONE"
            is_arch = bool(node.get("isArchived"))
            live_spdx[key] = (spdx_id, is_arch)

            if node.get("isDisabled") or node.get("isEmpty"):
                locs = ", ".join(f"{f}:{ln}" for f, ln, _, _ in repo_occurrences[key])
                errors.append(f"Disabled/empty GitHub repo {node['nameWithOwner']} at {locs}")
            if is_arch:
                for fname, ln, lbl, full_line in repo_occurrences[key]:
                    if fname == "README.md" and "archived" not in full_line.lower():
                        errors.append(
                            f"{fname}:{ln}: repo {node['nameWithOwner']} is archived on GitHub "
                            f"but not marked (Archived) on its row"
                        )
            rec = spdx_db.get(key)
            if not rec or rec.get("spdx") != spdx_id or bool(rec.get("archived")) != is_arch:
                errors.append(
                    f"GITHUB_SPDX.json mismatch for {key}: recorded={rec}, live=({spdx_id}, archived={is_arch})"
                )

    safe_txt = (ROOT / "catalogs" / "MIT_APACHE_COMMERCIAL_SAFE.md").read_text(encoding="utf-8")
    for lineno, line in enumerate(safe_txt.splitlines(), 1):
        for _, target in MD_LINK_RE.findall(strip_images(line)):
            sp = urlsplit(target)
            if sp.netloc.lower() == "github.com":
                parts = [p for p in sp.path.strip("/").split("/") if p]
                if len(parts) >= 2:
                    key = f"{parts[0].lower()}/{parts[1].lower().removesuffix('.git')}"
                    spdx_id, is_arch = live_spdx.get(key, ("UNKNOWN", True))
                    if spdx_id not in PERMISSIVE_SPDX or is_arch:
                        errors.append(
                            f"Live GitHub SPDX check failed on MIT_APACHE_COMMERCIAL_SAFE.md:{lineno}: "
                            f"{key} has spdx={spdx_id}, archived={is_arch}"
                        )

    return checked


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify-github", action="store_true", help="Verify all GitHub repos & SPDX licenses via gh CLI")
    args = parser.parse_args()

    errors: list[str] = []
    for req_file in (README, UNREAL_NOTES, GITHUB_SPDX_PATH):
        if not req_file.exists():
            errors.append(f"Missing {req_file.relative_to(ROOT).as_posix()}")
    if errors:
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    spdx_db = json.loads(GITHUB_SPDX_PATH.read_text(encoding="utf-8"))
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

    validate_public_hygiene(errors)
    r_urls = validate_readme(readme_text, errors)
    u_urls = validate_unreal_notes(notes_text, errors)
    validate_generated_indexes(spdx_db, errors)
    combined = r_urls | u_urls
    if len(combined) < 1190:
        errors.append(f"Expected >= 1190 non-badge unique HTTPS resource links matching badge claim, got {len(combined)}")

    gh_checked = 0
    if args.verify_github:
        gh_checked = verify_github_live(spdx_db, errors)

    if errors:
        print(f"VALIDATION FAILED with {len(errors)} error(s):", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    msg = (
        f"OK: README.md ({len(r_urls)} unique non-badge HTTPS links) + "
        f"catalogs/UNREAL.md ({len(u_urls)} unique HTTPS links) = "
        f"{len(combined)} unique resource links + 4 generated filter/JSON views validated cleanly."
    )
    if args.verify_github:
        msg += f" Live GitHub API verified {gh_checked} unique repositories & SPDX licenses."
    print(msg)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
