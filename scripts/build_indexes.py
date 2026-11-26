#!/usr/bin/env python3
from __future__ import annotations

import argparse
import dataclasses
import json
import pathlib
import re
import sys
from urllib.parse import urlsplit

ROOT = pathlib.Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
CATALOGS = ROOT / "catalogs"
GITHUB_SPDX_PATH = CATALOGS / "GITHUB_SPDX.json"

LINK_RE = re.compile(r"\[([^\]]+)\]\((https://[^)\s]+)\)")
SECTION_RE = re.compile(r"^## (\d+)\.\s+(.+?)\s*$")
DELIMITER_CELL_RE = re.compile(r"^:?-{3,}:?$")

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
VERIFIED_CC0_DOMAINS = frozenset({
    "polyhaven.com",
    "ambientcg.com",
    "kenney.nl",
    "kaylousberg.com",
    "quaternius.com",
})
VERIFIED_CC0_URLS = frozenset({
    "https://itch.io/game-assets/assets-cc0/free",
})
CODE_SOURCE_LANGS = frozenset({
    "C++",
    "C",
    "C#",
    "Objective-C",
    "Objective-C++",
    "Python",
    "Rust",
    "JavaScript",
    "TypeScript",
    "Lua",
    "HLSL",
    "GLSL",
    "Go",
    "Java",
    "Kotlin",
    "Haxe",
    "Nim",
})
PURE_BP_EPIC_SAMPLES = frozenset({
    "Stack-O-Bot",
    "Cropout Sample Project",
    "Multiplayer Shootout",
    "Epic Blueprints Showcase",
})
CODE_LANG_RE = re.compile(
    r"(?i)(?:(?<!\w)c\+\+|\bcpp\b|(?<!\w)c#|\bpython\b|\brust\b|\bangelscript\b|\bmcp\b|\bhlsl\b)"
)
NO_CPP_RE = re.compile(r"(?i)\b(?:no|zero)\s+c\+\+")


@dataclasses.dataclass(frozen=True)
class RawRow:
    section_number: int
    section_title: str
    name_raw: str
    name: str
    source_col: str
    meta: str
    highlights: str
    links_cell: str
    links: list[dict[str, str]]
    is_archived: bool


@dataclasses.dataclass(frozen=True)
class CatalogEntry:
    section_number: int
    section_title: str
    name: str
    meta: str
    highlights: str
    links_cell: str
    links: list[dict[str, str]]
    is_archived: bool
    is_ue58: bool
    is_commercial_safe: bool
    is_blueprint_first: bool


def clean_md(cell: str) -> str:
    return re.sub(r"\*+", "", cell).strip()


def gh_repo_key(url: str) -> str | None:
    sp = urlsplit(url)
    if sp.netloc.lower() != "github.com":
        return None
    parts = [p for p in sp.path.strip("/").split("/") if p]
    if len(parts) < 2 or parts[0].lower() in ("topics", "orgs", "users"):
        return None
    if len(parts) >= 4 and parts[2] == "actions":
        return None
    return f"{parts[0].lower()}/{parts[1].lower().removesuffix('.git')}"


def is_link_archived(link: dict[str, str], spdx_db: dict[str, dict[str, object]], row_name_archived: bool) -> bool:
    if row_name_archived or "archived" in link["label"].lower():
        return True
    key = gh_repo_key(link["url"])
    if key and key in spdx_db:
        return bool(spdx_db[key].get("archived"))
    return False


def link_permissive_spdx(url: str, spdx_db: dict[str, dict[str, object]]) -> str | None:
    norm = url.rstrip("/").lower()
    if norm in VERIFIED_CC0_URLS:
        return "CC0-1.0"
    sp = urlsplit(url)
    host = sp.netloc.lower().removeprefix("www.")
    if host in VERIFIED_CC0_DOMAINS:
        return "CC0-1.0"
    key = gh_repo_key(url)
    if key and key in spdx_db:
        info = spdx_db[key]
        if not info.get("archived") and not info.get("bundledRestriction"):
            spdx = str(info.get("spdx") or "")
            if spdx in PERMISSIVE_SPDX:
                return spdx
    return None


def is_link_ue58_verified(url: str, spdx_db: dict[str, dict[str, object]]) -> bool:
    key = gh_repo_key(url)
    if not key or key not in spdx_db:
        return False
    info = spdx_db[key]
    return bool(info.get("ue58Verified")) and not bool(info.get("archived")) and not bool(info.get("readmeOnly"))


def is_link_pure_blueprint(
    url: str,
    section_number: int,
    entry_name: str,
    spdx_db: dict[str, dict[str, object]],
) -> bool:
    key = gh_repo_key(url)
    if key:
        info = spdx_db.get(key)
        if not info or info.get("archived") or info.get("readmeOnly"):
            return False
        langs = info.get("languages") or []
        return not any(str(lang) in CODE_SOURCE_LANGS for lang in langs)
    if section_number == 1:
        return entry_name in PURE_BP_EPIC_SAMPLES
    return 2 <= section_number <= 21


def format_links(links: list[dict[str, str]]) -> str:
    return " · ".join(f"[{lk['label']}]({lk['url']})" for lk in links)


def parse_raw_rows(
    readme_text: str,
    spdx_db: dict[str, dict[str, object]],
) -> list[RawRow]:
    rows: list[RawRow] = []
    cur_num = 0
    cur_title = ""
    in_fence = False
    header_cols: list[str] = []
    table_row_idx = 0

    for lineno, raw_line in enumerate(readme_text.splitlines(), 1):
        line = raw_line.strip()
        if line.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue

        sec_match = SECTION_RE.match(line)
        if sec_match:
            cur_num = int(sec_match.group(1))
            cur_title = sec_match.group(2)
            header_cols = []
            table_row_idx = 0
            continue

        if cur_num == 0 or cur_num == 26:
            continue

        if line.startswith("|") and line.endswith("|"):
            cells = [c.strip() for c in line.strip("|").split("|")]
            if table_row_idx == 0:
                header_cols = [c.lower() for c in cells]
                table_row_idx = 1
                continue
            if table_row_idx == 1:
                if not all(DELIMITER_CELL_RE.match(c) for c in cells):
                    raise ValueError(f"README.md:{lineno}: missing or invalid Markdown table delimiter row")
                table_row_idx = 2
                continue

            links = [{"label": lbl, "url": url} for lbl, url in LINK_RE.findall(cells[-1])]
            if not links:
                continue

            name_raw = cells[0]
            source_col = ""
            if len(cells) == 5:
                source_col = cells[1]
                if "license" in header_cols[1]:
                    meta = f"{cells[2]} · {cells[1]}"
                else:
                    meta = cells[2]
                highlights = cells[3]
            elif len(cells) == 4:
                meta = cells[1]
                highlights = cells[2]
            elif len(cells) == 3:
                if cur_num == 1:
                    meta = "Official Epic Sample"
                elif cur_num == 22:
                    meta = "Commercial / Fab Reference"
                elif cur_num == 23:
                    meta = "Community Index / Guide"
                else:
                    meta = ""
                highlights = cells[1]
            else:
                continue

            row_name_archived = "archived" in name_raw.lower()
            active_links = [
                lk for lk in links if not is_link_archived(lk, spdx_db, row_name_archived)
            ]
            rows.append(
                RawRow(
                    section_number=cur_num,
                    section_title=cur_title,
                    name_raw=name_raw,
                    name=clean_md(name_raw),
                    source_col=source_col,
                    meta=meta,
                    highlights=highlights,
                    links_cell=cells[-1],
                    links=links,
                    is_archived=(len(active_links) == 0),
                )
            )
        else:
            header_cols = []
            table_row_idx = 0

    return rows


def dedup_links(links: list[dict[str, str]], seen_urls: set[str]) -> list[dict[str, str]]:
    kept: list[dict[str, str]] = []
    for lk in links:
        norm = lk["url"].rstrip("/").lower()
        if norm not in seen_urls:
            seen_urls.add(norm)
            kept.append(lk)
    return kept


def render_filtered_markdown(
    title: str,
    subtitle: str,
    rows_by_sec: dict[tuple[int, str], list[tuple[str, str, str, list[dict[str, str]]]]],
) -> str:
    total_rows = sum(len(v) for v in rows_by_sec.values())
    total_links = len({lk["url"].rstrip("/").lower() for v in rows_by_sec.values() for _, _, _, lks in v for lk in lks})
    lines = [
        f"# {title}",
        "",
        "[Back to main catalog](../README.md) · [Architecture Deep-Dives](UNREAL.md) · [UE 5.7–5.8 Ready](UE58_READY.md) · [MIT / Apache-2.0 Commercial-Safe](MIT_APACHE_COMMERCIAL_SAFE.md) · [Pure-Blueprint](BLUEPRINT_ONLY.md)",
        "",
        f"{subtitle} (**{total_rows} entries · {total_links} unique HTTPS links**, auto-synced from `README.md`).",
        "",
    ]
    for (snum, stitle), rows in sorted(rows_by_sec.items()):
        lines.append(f"## {snum}. {stitle}")
        lines.append("")
        lines.append("| Resource | UE / License | Highlights | Link |")
        lines.append("|---|---|---|---|")
        for name, meta, highlights, lks in rows:
            meta_disp = meta if meta else "See upstream"
            lines.append(f"| **{name}** | {meta_disp} | {highlights} | {format_links(lks)} |")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def compile_catalog(
    readme_text: str,
    spdx_db: dict[str, dict[str, object]],
) -> tuple[list[CatalogEntry], dict[pathlib.Path, str]]:
    raw_rows = parse_raw_rows(readme_text, spdx_db)

    ue58_sec: dict[tuple[int, str], list[tuple[str, str, str, list[dict[str, str]]]]] = {}
    ue58_seen: set[str] = set()
    emitted_ue58: set[int] = set()

    safe_sec: dict[tuple[int, str], list[tuple[str, str, str, list[dict[str, str]]]]] = {}
    safe_seen: set[str] = set()
    emitted_safe: set[int] = set()

    bp_sec: dict[tuple[int, str], list[tuple[str, str, str, list[dict[str, str]]]]] = {}
    bp_seen: set[str] = set()
    emitted_bp: set[int] = set()

    for idx, r in enumerate(raw_rows):
        if r.is_archived:
            continue
        row_arch = "archived" in r.name_raw.lower()
        active = [lk for lk in r.links if not is_link_archived(lk, spdx_db, row_arch)]

        # 1. Per-link upstream-verified UE 5.7 / 5.8 filter
        if r.section_number not in (22, 23, 27, 28, 29, 30, 31, 32):
            ue58_links = [lk for lk in active if is_link_ue58_verified(lk["url"], spdx_db)]
            chosen_ue58 = dedup_links(ue58_links, ue58_seen)
            if chosen_ue58:
                emitted_ue58.add(idx)
                meta_out = r.meta if ("5.7" in r.meta or "5.8" in r.meta) else "UE 5.7–5.8"
                ue58_sec.setdefault((r.section_number, r.section_title), []).append(
                    (r.name, meta_out, r.highlights, chosen_ue58)
                )

        # 2. Per-link SPDX & bundled-restriction verified Commercial-Safe filter
        if r.section_number not in (1, 22, 23):
            perm_links: list[dict[str, str]] = []
            perm_licenses: list[str] = []
            for lk in active:
                spdx = link_permissive_spdx(lk["url"], spdx_db)
                if spdx is not None:
                    perm_links.append(lk)
                    if spdx not in perm_licenses:
                        perm_licenses.append(spdx)
            chosen_safe = dedup_links(perm_links, safe_seen)
            if chosen_safe:
                emitted_safe.add(idx)
                safe_sec.setdefault((r.section_number, r.section_title), []).append(
                    (r.name, " / ".join(perm_licenses), r.highlights, chosen_safe)
                )

        # 3. Per-link GitHub-language-verified Pure-Blueprint filter (Sections 1..21)
        if 1 <= r.section_number <= 21 and "docs" not in r.source_col.lower():
            combined_text = f"{r.name_raw} {r.meta} {r.highlights}"
            mentions_code = bool(CODE_LANG_RE.search(combined_text)) and not bool(NO_CPP_RE.search(combined_text))
            has_bp_signal = (
                bool(re.search(r"(?<![/\w])BP(?![/\w])", r.meta))
                or "blueprint" in r.highlights.lower()
            )
            if has_bp_signal and not mentions_code:
                pure_bp_links = [
                    lk for lk in active
                    if is_link_pure_blueprint(lk["url"], r.section_number, r.name, spdx_db)
                ]
                chosen_bp = dedup_links(pure_bp_links, bp_seen)
                if chosen_bp:
                    emitted_bp.add(idx)
                    bp_sec.setdefault((r.section_number, r.section_title), []).append(
                        (r.name, r.meta, r.highlights, chosen_bp)
                    )

    entries = [
        CatalogEntry(
            section_number=r.section_number,
            section_title=r.section_title,
            name=r.name,
            meta=r.meta,
            highlights=r.highlights,
            links_cell=r.links_cell,
            links=r.links,
            is_archived=r.is_archived,
            is_ue58=(idx in emitted_ue58),
            is_commercial_safe=(idx in emitted_safe),
            is_blueprint_first=(idx in emitted_bp),
        )
        for idx, r in enumerate(raw_rows)
    ]

    all_urls = {lk["url"].rstrip("/").lower() for e in entries for lk in e.links}
    index_payload = {
        "schemaVersion": 3,
        "stats": {
            "tableBackedSections": len({e.section_number for e in entries}),
            "proseOrHardwareSections": [24, 26],
            "totalEntries": len(entries),
            "uniqueEntryLinks": len(all_urls),
            "ue57_58FilteredEntries": len(emitted_ue58),
            "commercialSafeFilteredEntries": len(emitted_safe),
            "pureBlueprintFilteredEntries": len(emitted_bp),
        },
        "entries": [dataclasses.asdict(e) for e in entries],
    }

    outputs = {
        CATALOGS / "UE58_READY.md": render_filtered_markdown(
            "UE 5.7 & UE 5.8 Verified Templates, Plugins & Tooling",
            "Filtered view of active Unreal Engine repositories verified upstream (`.uproject`/`.uplugin`/README) for **UE 5.7 or UE 5.8**",
            ue58_sec,
        ),
        CATALOGS / "MIT_APACHE_COMMERCIAL_SAFE.md": render_filtered_markdown(
            "Commercial-Safe Open-Source Stack (SPDX-Verified Permissive Licenses)",
            "Filtered view of active links verified via GitHub's License API (`MIT`, `Apache-2.0`, `BSD-2-Clause`, `BSD-3-Clause`, `0BSD`, `ISC`, `CC0-1.0`, `Unlicense`, `Zlib`, `BSL-1.0`, excluding bundled commercial/PolyForm restrictions) or pure `CC0` asset hubs — always verify third-party bundled content separately",
            safe_sec,
        ),
        CATALOGS / "BLUEPRINT_ONLY.md": render_filtered_markdown(
            "Pure-Blueprint Templates & Kits (No C++ Required)",
            "Filtered view of active **pure-Blueprint** starter templates and gameplay kits in Sections 1–21 verified with zero C++/C#/Python/Rust source modules on GitHub",
            bp_sec,
        ),
        CATALOGS / "INDEX.json": json.dumps(index_payload, indent=2, ensure_ascii=False) + "\n",
    }
    return entries, outputs


def parse_readme_entries(
    readme_text: str,
    spdx_db: dict[str, dict[str, object]] | None = None,
) -> list[CatalogEntry]:
    if spdx_db is None:
        spdx_db = json.loads(GITHUB_SPDX_PATH.read_text(encoding="utf-8"))
    entries, _ = compile_catalog(readme_text, spdx_db)
    return entries


def build_outputs(
    readme_text: str,
    spdx_db: dict[str, dict[str, object]],
) -> dict[pathlib.Path, str]:
    _, outputs = compile_catalog(readme_text, spdx_db)
    return outputs


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Verify generated indexes match README.md")
    args = parser.parse_args()

    if not GITHUB_SPDX_PATH.exists():
        print("Missing catalogs/GITHUB_SPDX.json", file=sys.stderr)
        return 1

    spdx_db = json.loads(GITHUB_SPDX_PATH.read_text(encoding="utf-8"))
    outputs = build_outputs(README.read_text(encoding="utf-8"), spdx_db)
    stale: list[str] = []
    for path, content in outputs.items():
        if args.check:
            if not path.exists() or path.read_text(encoding="utf-8") != content:
                stale.append(str(path.relative_to(ROOT)))
        else:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

    if stale:
        print(f"Index files out of sync with README.md: {', '.join(stale)}", file=sys.stderr)
        return 1

    stats = json.loads(outputs[CATALOGS / "INDEX.json"])["stats"]
    mode = "Checked" if args.check else "Generated"
    print(
        f"{mode} catalog indexes: {stats['totalEntries']} entries, "
        f"UE 5.7/5.8={stats['ue57_58FilteredEntries']}, "
        f"Commercial-Safe={stats['commercialSafeFilteredEntries']}, "
        f"Pure-Blueprint={stats['pureBlueprintFilteredEntries']}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
