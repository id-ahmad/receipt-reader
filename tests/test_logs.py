import json
import logging

import pytest

from receipt_reader import logs


def _last_line(capsys: pytest.CaptureFixture[str]) -> dict[str, object]:
    out: dict[str, object] = json.loads(capsys.readouterr().err.strip().splitlines()[-1])
    return out


def test_log_line_is_json_with_required_fields(capsys: pytest.CaptureFixture[str]) -> None:
    logs.configure()
    logs.log_event(logging.getLogger("test"), "model_called", "called haiku", latency_ms=812)

    line = _last_line(capsys)

    assert line["service"] == "receipt-reader"
    assert line["level"] == "info"
    assert line["event"] == "model_called"
    assert line["message"] == "called haiku"
    assert line["latency_ms"] == 812
    assert str(line["timestamp"]).endswith("+00:00")


def test_request_id_is_threaded_into_every_line(capsys: pytest.CaptureFixture[str]) -> None:
    logs.configure()
    token = logs.request_id.set("receipt-42")
    try:
        logs.log_event(logging.getLogger("test"), "check_failed", "sum mismatch", logging.WARNING)
    finally:
        logs.request_id.reset(token)

    line = _last_line(capsys)

    assert line["request_id"] == "receipt-42"
    assert line["level"] == "warn"
