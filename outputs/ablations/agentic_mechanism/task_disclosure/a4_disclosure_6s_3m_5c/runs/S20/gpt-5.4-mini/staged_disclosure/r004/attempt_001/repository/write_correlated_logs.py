import json
import os
import sys
import time
import uuid
from datetime import datetime, timezone

import requests


OPENAI_LOGS_API_URL = os.getenv("OPENAI_LOGS_API_URL", "https://api.openai.com/v1")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _build_event(level: str, message: str, correlation_id: str, request_id: str) -> dict:
    return {
        "provider": "openai",
        "level": level,
        "message": message,
        "correlation_id": correlation_id,
        "request_id": request_id,
        "timestamp": _now_iso(),
    }


def write_correlated_logs(message: str) -> int:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    correlation_id = str(uuid.uuid4())
    request_id = str(uuid.uuid4())

    session = requests.Session()
    session.headers.update(
        {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }
    )

    events = [
        _build_event("info", f"starting: {message}", correlation_id, request_id),
        _build_event("info", f"processing: {message}", correlation_id, request_id),
        _build_event("info", f"finished: {message}", correlation_id, request_id),
    ]

    for event in events:
        payload = {"input": json.dumps(event), "model": "gpt-5.4-mini"}
        response = session.post(f"{OPENAI_LOGS_API_URL}/responses", json=payload, timeout=30)
        response.raise_for_status()
        time.sleep(0.1)

    return 0


def main() -> int:
    message = sys.argv[1] if len(sys.argv) > 1 else "request"
    return write_correlated_logs(message)


if __name__ == "__main__":
    raise SystemExit(main())
