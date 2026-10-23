import json
import os
import uuid
from datetime import datetime, timezone

import requests


def _api_key() -> str:
    key = os.getenv("LOGTAIL_SOURCE_TOKEN") or os.getenv("LOGTAIL_API_KEY")
    if not key:
        raise RuntimeError("Missing LOGTAIL_SOURCE_TOKEN or LOGTAIL_API_KEY")
    return key


def _base_url() -> str:
    return os.getenv("LOGTAIL_BASE_URL", "https://in.logs.betterstack.com")


def _event(level: str, message: str, correlation_id: str, **fields):
    payload = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "level": level,
        "message": message,
        "correlation_id": correlation_id,
    }
    payload.update(fields)
    return payload


def write_correlated_logs(message: str, *, request_id: str | None = None, correlation_id: str | None = None, level: str = "info", **fields):
    cid = correlation_id or request_id or str(uuid.uuid4())
    events = [
        _event(level, "request received", cid, **fields),
        _event(level, message, cid, **fields),
        _event(level, "request completed", cid, **fields),
    ]
    response = requests.post(
        _base_url(),
        headers={
            "Authorization": f"Bearer {_api_key()}",
            "Content-Type": "application/json",
        },
        data=json.dumps(events),
        timeout=30,
    )
    response.raise_for_status()
    return {"correlation_id": cid, "status_code": response.status_code}


if __name__ == "__main__":
    raise SystemExit("Import and call write_correlated_logs()")
