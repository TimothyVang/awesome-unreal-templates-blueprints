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
UE58_TOKEN_RE = re.compile(
    r"\b5\.[78](?:\.\d+)?\b|5\.\d+[–-]5\.[78]|5\.x[–-]5\.[78]|4\.\d+[–-]5\.[78]"
)
CODE_LANG_RE = re.compile(r"(?i)(?:(?<!\w)c\+\+|\bcpp\b|(?<!\w)c#|\bpython\b|\brust\b|\bangelscript\b|\bmcp\b|\bhlsl\b)")
NO_CPP_RE = re.compile(r"(?i)\b(?:no|zero)\s+c\+\+")


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
        if not info.get("archived"):
            spdx = str(info.get("spdx") or "")
            if spdx in PERMISSIVE_SPDX:
                return spdx
    return None


def format_links(links: list[dict[str, str]]) -> str:
    return " · ".join(f"[{lk['label']}]({lk['url']})" for lk in links)


def parse_readme_entries(
    readme_text: str,
    spdx_db: dict[str, dict[str, object]],
) -> list[CatalogEntry]:
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
            is_archived = len(active_links) == 0

            meta_has_ue58 = bool(UE58_TOKEN_RE.search(meta))
            single_highlight_ue58 = len(links) == 1 and bool(UE58_TOKEN_RE.search(highlights))
            link_has_ue58 = any(UE58_TOKEN_RE.search(lk["label"]) for lk in active_links)
            is_ue58 = (
                not is_archived
                and cur_num not in (22, 23, 25, 27, 28, 29, 30, 31, 32)
                and (meta_has_ue58 or single_highlight_ue58 or link_has_ue58)
            )

            all_active_permissive = (
                not is_archived
                and cur_num not in (1, 22, 23)
                and all(link_permissive_spdx(lk["url"], spdx_db) is not None for lk in active_links)
            )

            combined_text = f"{meta} {highlights}"
            mentions_code = bool(CODE_LANG_RE.search(combined_text)) and not bool(NO_CPP_RE.search(combined_text))
            has_bp_signal = (
                bool(re.search(r"(?<![/\w])BP(?![/\w])", meta))
                or "blueprint" in highlights.lower()
            )
            is_bp = (
                not is_archived
                and 1 <= cur_num <= 21
                and has_bp_signal
                and not mentions_code
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
                    is_commercial_safe=all_active_permissive,
                    is_blueprint_first=is_bp,
                )
            )
        else:
            header_cols = []
            table_row_idx = 0

    return entries


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


def build_outputs(
    readme_text: str,
    spdx_db: dict[str, dict[str, object]],
) -> dict[pathlib.Path, str]:
    entries = parse_readme_entries(readme_text, spdx_db)

    ue58_sec: dict[tuple[int, str], list[tuple[str, str, str, list[dict[str, str]]]]] = {}
    ue58_seen: set[str] = set()
    for e in entries:
        if e.is_archived or e.section_number in (22, 23, 25, 27, 28, 29, 30, 31, 32):
            continue
        row_arch = "archived" in e.name.lower()
        active = [lk for lk in e.links if not is_link_archived(lk, spdx_db, row_arch)]
        if UE58_TOKEN_RE.search(e.meta) or (len(e.links) == 1 and UE58_TOKEN_RE.search(e.highlights)):
            chosen = dedup_links(active, ue58_seen)
        else:
            tagged = [lk for lk in active if UE58_TOKEN_RE.search(lk["label"])]
            chosen = dedup_links(tagged, ue58_seen)
        if chosen:
            meta_out = e.meta if UE58_TOKEN_RE.search(e.meta) else "UE 5.7–5.8"
            ue58_sec.setdefault((e.section_number, e.section_title), []).append(
                (e.name, meta_out, e.highlights, chosen)
            )

    safe_sec: dict[tuple[int, str], list[tuple[str, str, str, list[dict[str, str]]]]] = {}
    safe_seen: set[str] = set()
    for e in entries:
        if e.is_archived or e.section_number in (1, 22, 23, 25):
            continue
        row_arch = "archived" in e.name.lower()
        perm_links: list[dict[str, str]] = []
        perm_licenses: list[str] = []
        for lk in e.links:
            if is_link_archived(lk, spdx_db, row_arch):
                continue
            spdx = link_permissive_spdx(lk["url"], spdx_db)
            if spdx is not None:
                perm_links.append(lk)
                if spdx not in perm_licenses:
                    perm_licenses.append(spdx)
        chosen = dedup_links(perm_links, safe_seen)
        if chosen:
            lic_badge = " / ".join(perm_licenses)
            safe_sec.setdefault((e.section_number, e.section_title), []).append(
                (e.name, lic_badge, e.highlights, chosen)
            )

    bp_sec: dict[tuple[int, str], list[tuple[str, str, str, list[dict[str, str]]]]] = {}
    bp_seen: set[str] = set()
    for e in entries:
        if not e.is_blueprint_first:
            continue
        row_arch = "archived" in e.name.lower()
        active = [lk for lk in e.links if not is_link_archived(lk, spdx_db, row_arch)]
        chosen = dedup_links(active, bp_seen)
        if chosen:
            bp_sec.setdefault((e.section_number, e.section_title), []).append(
                (e.name, e.meta, e.highlights, chosen)
            )

    all_urls = {lk["url"].rstrip("/").lower() for e in entries for lk in e.links}
    ue58_count = sum(len(v) for v in ue58_sec.values())
    safe_count = sum(len(v) for v in safe_sec.values())
    bp_count = sum(len(v) for v in bp_sec.values())

    index_payload = {
        "schemaVersion": 2,
        "stats": {
            "tableBackedSections": len({e.section_number for e in entries}),
            "proseOrHardwareSections": [24, 26],
            "totalEntries": len(entries),
            "uniqueEntryLinks": len(all_urls),
            "ue57_58FilteredEntries": ue58_count,
            "commercialSafeFilteredEntries": safe_count,
            "pureBlueprintFilteredEntries": bp_count,
        },
        "entries": [dataclasses.asdict(e) for e in entries],
    }

    return {
        CATALOGS / "UE58_READY.md": render_filtered_markdown(
            "UE 5.7 & UE 5.8 Verified Templates, Plugins & Tooling",
            "Filtered view of active Unreal Engine resources explicitly targeting **UE 5.7 or UE 5.8**",
            ue58_sec,
        ),
        CATALOGS / "MIT_APACHE_COMMERCIAL_SAFE.md": render_filtered_markdown(
            "Commercial-Safe Open-Source Stack (SPDX-Verified Permissive Licenses)",
            "Filtered view of active links verified via GitHub's License API (`MIT`, `Apache-2.0`, `BSD-2-Clause`, `BSD-3-Clause`, `0BSD`, `ISC`, `CC0-1.0`, `Unlicense`, `Zlib`, `BSL-1.0`) or pure `CC0` asset hubs — always verify third-party bundled content separately",
            safe_sec,
        ),
        CATALOGS / "BLUEPRINT_ONLY.md": render_filtered_markdown(
            "Pure-Blueprint Templates, Kits & Node Libraries (No C++ Required)",
            "Filtered view of active **pure-Blueprint** gameplay starter templates, kits, and visual scripting libraries in Sections 1–21",
            bp_sec,
        ),
        CATALOGS / "INDEX.json": json.dumps(index_payload, indent=2, ensure_ascii=False) + "\n",
    }


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
