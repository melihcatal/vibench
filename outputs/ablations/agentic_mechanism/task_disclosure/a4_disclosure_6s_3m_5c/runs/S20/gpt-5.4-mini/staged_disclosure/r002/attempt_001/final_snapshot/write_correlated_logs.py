import json
import os
import uuid
from datetime import datetime, timezone

import requests


DATADOG_API_HOST = "https://http-intake.logs.datadoghq.com"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _build_log(level: str, message: str, request_id: str, span_id: str) -> dict:
    return {
        "timestamp": _now_iso(),
        "service": os.getenv("DD_SERVICE", "correlated-logs-demo"),
        "env": os.getenv("DD_ENV", "dev"),
        "logger": "write_correlated_logs",
        "level": level,
        "message": message,
        "request_id": request_id,
        "span_id": span_id,
        "dd.source": "python",
        "dd.tags": f"request_id:{request_id},span_id:{span_id}",
    }


def write_correlated_logs() -> None:
    api_key = os.getenv("DATADOG_API_KEY")
    if not api_key:
        raise RuntimeError("DATADOG_API_KEY is required")

    request_id = str(uuid.uuid4())
    span_id = str(uuid.uuid4())

    events = [
        _build_log("info", "request received", request_id, span_id),
        _build_log("info", "validated request payload", request_id, span_id),
        _build_log("info", "request completed", request_id, span_id),
    ]

    payload = "\n".join(json.dumps(event, separators=(",", ":")) for event in events)
    headers = {
        "DD-API-KEY": api_key,
        "Content-Type": "application/json",
    }
    response = requests.post(DATADOG_API_HOST, data=payload, headers=headers, timeout=10)
    response.raise_for_status()


if __name__ == "__main__":
    write_correlated_logs()
