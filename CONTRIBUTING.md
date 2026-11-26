# Contributing to Awesome Unreal Templates, Blueprints & Pro Frameworks

Contributions of high-signal Unreal Engine 5 templates, Blueprint systems, open-source C++/GAS plugins, and Blender ↔ UE5 pipeline tools are welcome!

## Quality & Inclusion Criteria

1. **Direct Inspectability:** Entries must point to a real, publicly accessible source repository (GitHub/GitLab), official Epic Games / studio documentation page, or verified free/reference listing. Empty placeholder repos, dead links, or unauthorized asset rips are not accepted.
2. **Explicit License & Status Honesty:**
   - Check the repository's `LICENSE` file before labeling it `MIT`, `Apache-2.0`, `BSD-3-Clause`, `MPL-2.0`, or `GPL-2.0/3.0`.
   - Remember that a repository code license does not automatically cover bundled third-party art, storefront entitlements, or cloud service terms.
   - If a repository is archived on GitHub, include `*(Archived)*` on the entry so readers know its maintenance status upfront.
3. **Engine Version Context:** When a project's `.uproject` or `.uplugin` explicitly targets a modern version (such as **UE 5.7** or **UE 5.8**), note it in the `UE / License` column.
4. **No Same-Section Duplicates:** Each resource should appear once in its primary category (cross-references in pipeline architecture overviews are fine).

## Formatting & Local Validation

Before opening a Pull Request, run the zero-dependency Python 3 validator from the repository root:

```bash
python3 scripts/validate_catalog.py
```

If you have the GitHub CLI (`gh`) authenticated locally, you can also verify all GitHub repositories against the live GraphQL API (checking for 404s, disabled/empty repos, and unmarked archived repos):

```bash
python3 scripts/validate_catalog.py --verify-github
```
