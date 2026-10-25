"""Structured JSON logging: one JSON object per line, same format locally and in CI.

Follows ~/ai_project/guidelines/observability.md. Every line carries timestamp, level,
request_id, service, event and message, plus event-specific fields. Here a "request" is
one receipt going through one system, so request_id ties together every line it triggers.
"""

import contextvars
import json
import logging
import sys
from datetime import UTC, datetime
from typing import Any

SERVICE = "receipt-reader"

request_id: contextvars.ContextVar[str | None] = contextvars.ContextVar("request_id", default=None)

_LEVEL_NAMES = {
    logging.DEBUG: "debug",
    logging.INFO: "info",
    logging.WARNING: "warn",
    logging.ERROR: "error",
    logging.CRITICAL: "error",
}


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        line: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, UTC).isoformat(),
            "level": _LEVEL_NAMES.get(record.levelno, record.levelname.lower()),
            "request_id": request_id.get(),
            "service": SERVICE,
            "event": getattr(record, "event", record.name),
            "message": record.getMessage(),
        }
        line.update(getattr(record, "fields", {}))
        if record.exc_info:
            line["exception"] = self.formatException(record.exc_info)
        return json.dumps(line, default=str)


def configure(level: int = logging.INFO) -> None:
    """Send all logs to stderr as JSON lines. Call once at program start."""
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(JsonFormatter())
    root = logging.getLogger()
    root.handlers[:] = [handler]
    root.setLevel(level)


def log_event(
    logger: logging.Logger,
    event: str,
    message: str,
    level: int = logging.INFO,
    **fields: Any,
) -> None:
    """Log one event with its fields, e.g. log_event(log, "model_called", "...", latency_ms=812)."""
    logger.log(level, message, extra={"event": event, "fields": fields})
