# receipt-reader

Receipt photo in, structured JSON out: OCR baseline vs open-weight vision model on Modal vs Claude, plus a cost-aware router, measured on CORD v2.

## Status

Project setup done; building the data loader and scoring next. See [`project/`](./project/) for vision, decisions, journal and backlog.

## Setup

Requires [uv](https://docs.astral.sh/uv/).

```bash
uv sync                      # create .venv and install everything
uv run ruff check            # lint
uv run ruff format --check   # formatting
uv run mypy                  # type check
uv run pytest                # tests
```

## Data

This project uses **CORD v2** ([`naver-clova-ix/cord-v2`](https://huggingface.co/datasets/naver-clova-ix/cord-v2)),
released by NAVER Clova under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/):

> Park, S., Shin, S., Lee, B., Lee, J., Surh, J., Seo, M., & Lee, H. (2019).
> *CORD: A Consolidated Receipt Dataset for Post-OCR Parsing.*
> Document Intelligence Workshop at NeurIPS 2019.

The data is downloaded by a script, never committed.

## Licence

Code: [MIT](./LICENSE). The CORD data keeps its own licence (CC BY 4.0, above).
