# Backlog

## Now (v1)

- [x] Target schema (ADR 0001)
- [x] Project setup: uv, Ruff, mypy, pytest, JSON logging, CI
- [x] Data loader: download CORD, convert ground truth to the target schema, normalise amounts (ADR 0002, 0003)
- [ ] Scoring: per-field precision / recall / F1, receipt-level exact match
- [ ] System 0: OCR baseline + rules
- [ ] System 2: Claude with structured outputs (Haiku / Sonnet / Opus)
- [ ] System 1: open-weight vision model on Modal
- [ ] Tracing (Langfuse, to confirm)
- [ ] Router (cascade) + "one strong model at low effort" comparison
- [ ] One command: download → all systems on test → report
- [ ] Real end-to-end run (real API, real GPU)
- [ ] Abdel's write-up
- [ ] Update `TRACKER.md` and the round's count table

## Next (post-v1)

- [ ] P1b: fine-tuning, reusing this harness

## Later (v2+)

- [ ] <task>
