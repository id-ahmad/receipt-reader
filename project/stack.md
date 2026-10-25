# Stack & architecture

## High-level shape

```
CORD v2 (Hugging Face) ──► loader + normalisation ──► receipts in the target schema (ADR 0001)
                                                              │
receipt photo ──► system ──► JSON in the target schema ───────┤
   systems: OCR baseline · open-weight VLM on Modal ·         ▼
            Claude (structured outputs) · router        scorer ──► report
                                                     (accuracy, cost, latency)
every model call ──► tracing (Langfuse, to confirm)
```

## Tech choices

- Language: Python 3.12, managed with uv
- Schema / validation: Pydantic
- Tests / lint / types: pytest · Ruff · mypy (strict)
- LLM provider: Anthropic API (Claude), plus an open-weight vision model served on Modal
- GPU hosting: Modal (Abdel's accounts; ask which before deploying)
- Tracing: Langfuse (to confirm)
- Logging: JSON lines per `~/ai_project/guidelines/observability.md` (`src/receipt_reader/logs.py`)
- CI: GitHub Actions — lint, format, type check, tests on every push and PR
- Interface: CLI only

## Constraints

- Budget: D5's €50/month ceiling; set the Anthropic console spend limit before the first paid run.
- Modal: short `scaledown_window`; state a run's cost before running it.
- Test split touched for final numbers only.
