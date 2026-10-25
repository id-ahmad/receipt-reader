# CLAUDE.md — context for Claude Code

## Project: receipt-reader

Receipt photo in, structured JSON out: OCR baseline vs open-weight vision model on Modal vs Claude, plus a cost-aware router, measured on CORD v2.

**Start here:** [`~/ai_project/applied_ai_path/notes/receipt-reader-brief.md`](~/ai_project/applied_ai_path/notes/receipt-reader-brief.md). It holds every decision already made: systems to compare, data, metrics, what "done" means, stack, budget. Build it; don't re-decide it. This is Round 1, project P1 of Abdel's applied AI portfolio (`~/ai_project/applied_ai_path/rounds/01-adenes/`). P1b (fine-tuning) will live in this repo too.

## Standing rules (from the portfolio session — this repo doesn't see its memory)

- **Abdel is learning; he's new to the LLM side.** Explain each concept in plain words before using it, and add every new term to `~/ai_project/applied_ai_path/glossary.md`. Let him make the choices that teach something: explain the trade-off, recommend, let him decide. **The write-ups are his**, in his own words.
- **Git identity:** `id-ahmad` + `67088734+id-ahmad@users.noreply.github.com`, set per repo. Never a personal or work address. Check `git log --format='%an %ae' | sort -u` before any push.
- **Browser work** (Langfuse UI, screenshots): Abdel's **personal** Chrome ("personal ai" profile) only, never the work browser. Check `list_connected_browsers` first.
- **Modal:** ask which account before deploying. Keep `scaledown_window` short. State a run's cost before running it.
- **Done means a real end-to-end run** (real API, real GPU), not only tests against fakes.
- **No dates or schedules. Real numbers only**, never invented ones.
- **When a project finishes**, update `~/ai_project/applied_ai_path/TRACKER.md` and the count table in `~/ai_project/applied_ai_path/rounds/01-adenes/README.md`.

## How to work in this repo

1. **Read `project/` before suggesting anything.** All scope, decisions, and constraints live there.
2. **Start each session by reading the latest entry in `project/journal/`.** Tells you what happened last time.
3. **End each session by writing a new entry in `project/journal/`.** Use `project/_templates/journal-entry.md`.
4. **Decisions are immutable.** ADRs in `project/decisions/` are never edited or deleted. If a decision changes, write a new ADR that supersedes the old one and update the old `status:` to `superseded by NNNN`.
5. **Captured constraints stay captured.** If `project/vision.md` says something is out of v1 scope, don't suggest building it for v1 without an explicit scope-change decision.

## Cross-project guidelines

This project follows the conventions in `~/ai_project/guidelines/`:
- [project-structure.md](~/ai_project/guidelines/project-structure.md) — folder layout
- [observability.md](~/ai_project/guidelines/observability.md) — logging & instrumentation rules
- [deployment-and-maintenance.md](~/ai_project/guidelines/deployment-and-maintenance.md) — autonomous error → fix → deploy chain

Read those if you haven't recently.

## Conventions

- Markdown for all project docs.
- Kebab-case filenames.
- YAML frontmatter on specs and ADRs: `status`, `date`, `owner`.
- New ADR? Use the next sequential number, copy from `project/_templates/decision.md`.
- New spec? Copy from `project/_templates/spec.md` and add to `project/specs/_index.md`.

## Commands

<Fill in once implementation starts. Examples:>
- `npm run dev` — start local dev server
- `npm test` — run tests
- `npm run deploy` — deploy to production
