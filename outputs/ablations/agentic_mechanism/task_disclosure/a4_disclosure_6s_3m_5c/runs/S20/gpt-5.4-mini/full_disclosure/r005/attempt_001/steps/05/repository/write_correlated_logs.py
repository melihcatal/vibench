import json
import os
from datetime import datetime, timezone

import requests


def _base_url() -> str:
    return os.environ.get("DATADOG_LOGS_API_URL", "https://http-intake.logs.datadoghq.com/api/v2/logs")


def _api_key() -> str:
    key = os.environ.get("DATADOG_API_KEY")
    if not key:
        raise RuntimeError("DATADOG_API_KEY is required")
    return key


def _correlation_id() -> str:
    return os.environ.get("REQUEST_ID") or os.environ.get("CORRELATION_ID") or os.urandom(16).hex()


def write_correlated_logs(message: str, level: str = "info", service: str = "application") -> dict:
    correlation_id = _correlation_id()
    payload = {
        "data": [
            {
                "ddsource": "python",
                "service": service,
                "message": message,
                "status": level,
                "ddtags": f"correlation_id:{correlation_id}",
                "attributes": {
                    "correlation_id": correlation_id,
                    "request_id": correlation_id,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                },
            }
        ]
    }
    response = requests.post(
        _base_url(),
        headers={
            "Content-Type": "application/json",
            "DD-API-KEY": _api_key(),
        },
        data=json.dumps(payload),
        timeout=30,
    )
    response.raise_for_status()
    return {"correlation_id": correlation_id, "status_code": response.status_code}
