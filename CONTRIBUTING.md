# Contributing to Awesome Unreal Templates, Blueprints & Pro Frameworks

Contributions of high-signal Unreal Engine 5 templates, Blueprint systems, open-source C++/GAS plugins, UEFN/Verse libraries, and Blender ↔ UE5 pipeline tools are welcome!

## Quality & Inclusion Criteria

1. **Direct Inspectability:** Entries must point to a real, publicly accessible source repository (GitHub/GitLab), official Epic Games / studio documentation page, or verified free/reference listing. Empty placeholder repos, dead links, live-memory game-hacking dumpers, or unauthorized asset rips are not accepted.
2. **Explicit License & Status Honesty:**
   - Check the repository's `LICENSE` file before labeling it `MIT`, `Apache-2.0`, `BSD-3-Clause`, `MPL-2.0`, or `GPL-2.0/3.0`, and record any newly added GitHub repository's SPDX license and archive state in `catalogs/GITHUB_SPDX.json`.
   - Remember that a repository code license does not automatically cover bundled third-party art, storefront entitlements, or cloud service terms.
   - If a repository is archived on GitHub, include `*(Archived)*` on the entry so readers know its maintenance status upfront.
3. **Engine Version Context:** When a project's `.uproject` or `.uplugin` explicitly targets a modern version (such as **UE 5.7** or **UE 5.8**), note it in the `UE / License` column.
4. **No Same-Section Duplicates:** Each resource should appear once in its primary category (cross-references in pipeline architecture overviews are fine).

## Regenerating Filter Views & Validating Locally

`README.md` + `catalogs/GITHUB_SPDX.json` drive the auto-generated filter catalogs (`catalogs/UE58_READY.md`, `catalogs/MIT_APACHE_COMMERCIAL_SAFE.md`, `catalogs/BLUEPRINT_ONLY.md`) and `catalogs/INDEX.json`.

After editing `README.md` or `catalogs/GITHUB_SPDX.json`, regenerate the filter views and run the zero-dependency Python 3 validator:

```bash
python3 -B scripts/build_indexes.py
python3 -B scripts/validate_catalog.py
```

If you have the GitHub CLI (`gh`) authenticated locally, verify all GitHub repositories and SPDX licenses against the live GraphQL API:

```bash
python3 -B scripts/validate_catalog.py --verify-github
```
