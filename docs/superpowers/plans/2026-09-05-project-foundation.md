# Project Foundation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a private, reviewable repository that stores the five-language SEO/AEO audit, plain-language project plan, visual workflows, and reproducible validation metadata.

**Architecture:** Keep human-readable guidance in `docs`, curated evidence in `audit`, image approval states in `assets`, and verification code in `tools` and `tests`. Keep the full local HTML archive out of Git while preserving relative paths, byte sizes, and SHA-256 hashes.

**Tech Stack:** Git/GitHub, Markdown, Mermaid, Python 3.12 standard library

**Spec:** `docs/superpowers/specs/2026-09-05-project-foundation-design.md`

## Global Constraints

- Scope is `kr`, `en`, `jp`, `cn`, and `tw`; Thailand is excluded.
- Do not store credentials, cookies, tokens, patient data, or unapproved people images.
- Do not save, publish, or change permissions in Imweb.
- Do not include the local `*.html.gz` source archive in Git.
- Present existing-file diffs before modification and run validation before completion claims.

---

### Task 1: Plain-language project documentation

**Files:**
- Modify: `README.md`
- Create: `.github/pr-body.md`
- Create: `docs/01-PRD.md`
- Create: `docs/02-TECH-STACK.md`
- Create: `docs/03-ARCHITECTURE.md`
- Create: `docs/04-WORKFLOW.md`
- Create: `docs/05-CLAUDE-CODE-INSTRUCTIONS.md`
- Create: `docs/06-REVIEW-LOG.md`
- Create: `docs/PROJECT-MAP.md`

**Interfaces:**
- Consumes: Verified audit facts in `audit/data/summary.json` and `audit/data/validated-urls.json`.
- Produces: The reading path and safety rules used by later SEO and image plans.

- [ ] **Step 1: Add the seven required documents in the AGENTS.md order**

Write the PRD, tool explanation, architecture, workflow, Claude Code instructions, review log, and visual map with explicit five-language scope and no live-site completion claim.

- [ ] **Step 2: Add GitHub-rendered Mermaid diagrams**

Add at least seven `mermaid` blocks across README and `docs/*.md`, covering the project overview, branch isolation, evidence flow, implementation workflow, responsibilities, safety loop, and image approval flow.

- [ ] **Step 3: Run the document checks**

Run: `python -X utf8 -c "from pathlib import Path; root=Path('.'); required=['docs/01-PRD.md','docs/02-TECH-STACK.md','docs/03-ARCHITECTURE.md','docs/04-WORKFLOW.md','docs/05-CLAUDE-CODE-INSTRUCTIONS.md','docs/06-REVIEW-LOG.md','docs/PROJECT-MAP.md']; marker=chr(96)*3+'mermaid'; assert all((root/p).is_file() for p in required); assert sum(p.read_text(encoding='utf-8').count(marker) for p in (root/'docs').glob('*.md')) >= 7; print('documents=7, mermaid>=7')"`

Expected: `documents=7, mermaid>=7` and exit code 0.

- [ ] **Step 4: Commit**

Run: `git add README.md docs assets/README.md .github/pr-body.md && git commit -m "docs: add plain-language project foundation"`

Expected: one documentation commit on `docs/project-foundation`.

### Task 2: Curated audit data and provenance

**Files:**
- Create: `audit/reports/INITIAL-AUDIT-KO.md`
- Create: `audit/reports/PRE-CHANGE-CODE-REVIEW-KO.md`
- Create: `audit/reports/VERIFICATION-LOG-KO.md`
- Create: `audit/data/summary.json`
- Create: `audit/data/browser-observations.json`
- Create: `audit/data/validated-urls.json`
- Create: `audit/data/javascript-syntax-check.json`
- Create: `audit/data/source-evidence-manifest.csv`
- Create: `audit/inventories/*.csv`
- Create: `tools/prepare_repository_data.py`
- Create: `tests/test_repository.py`

**Interfaces:**
- Consumes: Local read-only audit directory supplied as the first command argument.
- Produces: `validated-urls.json` and `source-evidence-manifest.csv` without absolute local paths or raw HTML bodies.

- [ ] **Step 1: Generate the curated URL record and source manifest**

Run: `python -X utf8 tools/prepare_repository_data.py ../../../audit .`

Expected: JSON output reports 9 validated URLs and a nonzero manifest file count.

- [ ] **Step 2: Validate the audit counts and provenance**

Run: `python -X utf8 -W error::ResourceWarning -m unittest discover -s tests -v`

Expected: 8 tests pass and 0 fail.

- [ ] **Step 3: Confirm raw HTML is absent**

Run: `python -X utf8 -m unittest discover -s tests -k no_absolute_local_links_or_raw_html_archive -v`

Expected: 1 test passes and 0 fail.

- [ ] **Step 4: Commit**

Run: `git add audit tools tests && git commit -m "data: add curated five-language audit snapshot"`

Expected: one data commit on `docs/project-foundation`.

### Task 3: Reviewable GitHub handoff

**Files:**
- Modify: no project files
- Test: `tests/test_repository.py`

**Interfaces:**
- Consumes: All files produced by Tasks 1 and 2.
- Produces: A pushed branch and unmerged pull request for human review.

- [ ] **Step 1: Run all repository tests**

Run: `python -X utf8 -W error::ResourceWarning -m unittest discover -s tests -v`

Expected: 8 tests pass and 0 fail.

- [ ] **Step 2: Check Markdown links and Git whitespace**

Run: `git diff --check main...HEAD`

Expected: no output and exit code 0.

- [ ] **Step 3: Push the planning branch**

Run: `git push -u origin docs/project-foundation`

Expected: remote branch `docs/project-foundation` is created.

- [ ] **Step 4: Open a pull request without merging**

Run: `gh pr create --base main --head docs/project-foundation --title "docs: add SEO/AEO project foundation" --body-file .github/pr-body.md`

Expected: GitHub returns a pull request URL. Leave it open for user review.
