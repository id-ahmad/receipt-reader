# Open questions

Unresolved questions that don't block scaffolding but need answers before / during implementation.

## Product

- Which OCR engine for the baseline: Tesseract, PaddleOCR or docTR?
- Which open-weight vision model: Qwen3.5-4B, Ministral 3 8B, or an OCR model feeding a text model?

## Technical

- Tracing: confirm Langfuse (the brief's proposal) at the start of the model work.
- Scoring details left open by ADR 0001: name comparison (incl. empty names from ADR 0003), items with no count, matching predicted items to true items.

## Legal / policy

- Anthropic console spend limit (D5) set before the first paid API run?
