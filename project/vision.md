# Vision

## What is receipt-reader?

Receipt photo in, structured JSON out: OCR baseline vs open-weight vision model on Modal vs Claude, plus a cost-aware router, measured on CORD v2.

The full brief (systems, data, metrics, "done", budget) is
[`~/ai_project/applied_ai_path/notes/receipt-reader-brief.md`](../../applied_ai_path/notes/receipt-reader-brief.md).
This file doesn't repeat it.

## Why?

The goal is Abdel learning transferable AI skills: defining an extraction task, building an
eval, comparing open-weight vs API models on accuracy, cost and latency, routing between
them, and tracing every call. The receipt reader is the vehicle. It's project P1 of Round 1
of the applied AI portfolio (`~/ai_project/applied_ai_path/rounds/01-adenes/`).

## Who is it for?

Abdel, as evidence of skill (public repo, his own write-up). Not a product for end users.

## Success criteria for v1

The "What done means" checklist in the brief: one command reproduces download → every
system on the test split → report; real numbers on accuracy, cost and latency; router vs
one strong model at low effort; tests + CI; a real end-to-end run on the real API and a
real Modal GPU; Abdel's write-up.

## Non-goals (v1)

Fine-tuning (that's P1b, same repo), RAG, agents, MCP, any web service (a CLI is enough).
