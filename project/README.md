# project/

Internal strategy and live state. This drives the work; `docs/` (when it exists) will be user-facing.

## Folder map

| Path | Purpose |
|---|---|
| `vision.md` | Why we're building this, success criteria, non-goals |
| `stack.md` | Tech stack + high-level architecture sketch |
| `backlog.md` | Prioritized: now / next / later |
| `issues.md` | Known bugs and problems (flat list; promote to file if complex) |
| `questions.md` | Open unknowns |
| `specs/` | One file per feature/module |
| `decisions/` | ADRs: one file per decision, numbered, immutable |
| `journal/` | Session log |
| `_templates/` | Skeletons for new specs/ADRs/journal entries |

## Conventions

- Markdown only. Kebab-case filenames.
- `_index.md` in each subfolder lists what's there with status. Keep current.
- ADRs are immutable. Supersede with a new ADR.
- Frontmatter on specs and ADRs: `status`, `date`, `owner`.
- One source of truth per fact. Link, don't duplicate.

See `~/ai_project/guidelines/project-structure.md` for full conventions.

## Session protocol

**Start:** read latest `journal/` entry → check `backlog.md` → read relevant `specs/`.

**End:** update `backlog.md` → update `issues.md` → write new `journal/YYYY-MM-DD.md` → ADR if a non-trivial decision was made.
