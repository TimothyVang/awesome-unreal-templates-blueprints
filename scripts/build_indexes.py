#!/usr/bin/env python3
from __future__ import annotations

import argparse
import dataclasses
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
README = ROOT / "README.md"
CATALOGS = ROOT / "catalogs"

LINK_RE = re.compile(r"\[([^\]]+)\]\((https://[^)\s]+)\)")
SECTION_RE = re.compile(r"^## (\d+)\.\s+(.+?)\s*$")
COMMERCIAL_SAFE_RE = re.compile(r"\b(MIT|Apache-2\.0|BSD(?:-2-Clause|-3-Clause)?|CC0(?:-1\.0)?|Unlicense|Zlib|BSL-1\.0)\b")
COPYLEFT_OR_CUSTOM_RE = re.compile(r"(?i)\b(GPL|AGPL|LGPL|Custom|Dual License)\b")
UE58_RE = re.compile(r"\bUE\s*5\.[78]\b|\b5\.[78]\+|\(5\.[78]\)|5\.0–5\.8|5\.3–5\.8|5\.4–5\.8|5\.5–5\.8|5\.6–5\.8|5\.7–5\.8")
BP_FIRST_RE = re.compile(r"\bBP\b|\bBlueprints?\b", re.IGNORECASE)


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


def parse_readme_entries(readme_text: str) -> list[CatalogEntry]:
    entries: list[CatalogEntry] = []
    cur_num = 0
    cur_title = ""
    in_fence = False
    header_cols: list[str] = []
    table_row_idx = 0

    for raw_line in readme_text.splitlines():
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
                table_row_idx = 2
                continue

            links = [{"label": lbl, "url": url} for lbl, url in LINK_RE.findall(cells[-1])]
            if not links:
                continue

            name_raw = cells[0]
            if len(cells) == 5:
                if "license" in header_cols[1]:
                    meta = f"{cells[2]} · {cells[1]}"
                else:
                    meta = cells[2]
                highlights = cells[3]
            elif len(cells) == 4:
                meta = cells[1]
                highlights = cells[2]
            elif len(cells) == 3:
                meta = "Official / Reference" if cur_num in (1, 22, 23) else ""
                highlights = cells[1]
            else:
                continue

            joined_row = f"{name_raw} | {meta} | {highlights} | {cells[-1]}"
            is_archived = "archived" in joined_row.lower()
            is_ue58 = bool(UE58_RE.search(joined_row))
            is_commercial_safe = (
                cur_num != 22
                and bool(COMMERCIAL_SAFE_RE.search(meta))
                and not COPYLEFT_OR_CUSTOM_RE.search(meta)
            )
            is_bp = (
                cur_num not in (22, 26, 27, 28, 29, 30, 31, 32)
                and (
                    bool(re.search(r"(?<![/\w])BP(?![/\w])", meta))
                    or ("blueprint" in highlights.lower() and "c++" not in meta.lower())
                )
            )

            entries.append(
                CatalogEntry(
                    section_number=cur_num,
                    section_title=cur_title,
                    name=clean_md(name_raw),
                    meta=meta,
                    highlights=highlights,
                    links_cell=cells[-1],
                    links=links,
                    is_archived=is_archived,
                    is_ue58=is_ue58,
                    is_commercial_safe=is_commercial_safe,
                    is_blueprint_first=is_bp,
                )
            )
        else:
            header_cols = []
            table_row_idx = 0

    return entries


def render_filtered_markdown(
    title: str,
    subtitle: str,
    entries: list[CatalogEntry],
) -> str:
    by_sec: dict[tuple[int, str], list[CatalogEntry]] = {}
    for e in entries:
        by_sec.setdefault((e.section_number, e.section_title), []).append(e)

    total_links = len({lk["url"].rstrip("/").lower() for e in entries for lk in e.links})
    lines = [
        f"# {title}",
        "",
        "[Back to main catalog](../README.md) · [Architecture Deep-Dives](UNREAL.md) · [UE 5.7–5.8 Ready](UE58_READY.md) · [MIT / Apache-2.0 Commercial-Safe](MIT_APACHE_COMMERCIAL_SAFE.md) · [Blueprint-First](BLUEPRINT_ONLY.md)",
        "",
        f"{subtitle} (**{len(entries)} entries · {total_links} unique HTTPS links**, auto-synced from `README.md`).",
        "",
    ]
    for (snum, stitle), rows in sorted(by_sec.items()):
        lines.append(f"## {snum}. {stitle}")
        lines.append("")
        lines.append("| Resource | UE / License | Highlights | Link |")
        lines.append("|---|---|---|---|")
        for r in rows:
            name_disp = f"**{r.name}**"
            meta_disp = r.meta if r.meta else "See upstream"
            lines.append(f"| {name_disp} | {meta_disp} | {r.highlights} | {r.links_cell} |")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def build_outputs(readme_text: str) -> dict[pathlib.Path, str]:
    entries = parse_readme_entries(readme_text)
    ue58_entries = [e for e in entries if e.is_ue58 and not e.is_archived]
    safe_entries = [e for e in entries if e.is_commercial_safe and not e.is_archived]
    bp_entries = [e for e in entries if e.is_blueprint_first and not e.is_archived]

    all_urls = {lk["url"].rstrip("/").lower() for e in entries for lk in e.links}
    index_payload = {
        "schemaVersion": 1,
        "stats": {
            "sections": len({e.section_number for e in entries}),
            "totalEntries": len(entries),
            "uniqueEntryLinks": len(all_urls),
            "ue57_58Entries": len(ue58_entries),
            "commercialSafeEntries": len(safe_entries),
            "blueprintFirstEntries": len(bp_entries),
        },
        "entries": [dataclasses.asdict(e) for e in entries],
    }

    return {
        CATALOGS / "UE58_READY.md": render_filtered_markdown(
            "UE 5.7 & UE 5.8 Verified Templates, Plugins & Tooling",
            "Filtered view of active resources explicitly targeting **Unreal Engine 5.7 or 5.8**",
            ue58_entries,
        ),
        CATALOGS / "MIT_APACHE_COMMERCIAL_SAFE.md": render_filtered_markdown(
            "Commercial-Safe Open-Source Stack (MIT / Apache-2.0 / BSD / CC0)",
            "Filtered view of active resources carrying permissive repository code licenses (`MIT`, `Apache-2.0`, `BSD`, `CC0`, `Unlicense`, `Zlib`, `BSL-1.0` — always verify third-party bundled content separately)",
            safe_entries,
        ),
        CATALOGS / "BLUEPRINT_ONLY.md": render_filtered_markdown(
            "Blueprint-First Templates, Kits & Node Libraries",
            "Filtered view of active **Blueprint-first** starter templates, gameplay kits, and visual scripting node libraries",
            bp_entries,
        ),
        CATALOGS / "INDEX.json": json.dumps(index_payload, indent=2, ensure_ascii=False) + "\n",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="Verify generated indexes match README.md")
    args = parser.parse_args()

    outputs = build_outputs(README.read_text(encoding="utf-8"))
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
        f"UE 5.7/5.8={stats['ue57_58Entries']}, "
        f"Commercial-Safe={stats['commercialSafeEntries']}, "
        f"Blueprint-First={stats['blueprintFirstEntries']}."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
