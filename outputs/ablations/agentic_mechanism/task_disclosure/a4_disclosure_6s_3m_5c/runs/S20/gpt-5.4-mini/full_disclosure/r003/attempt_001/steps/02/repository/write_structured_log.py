import json
import os
from datetime import datetime, timezone

import requests


LOGTAIL_SOURCE_TOKEN_ENV = "LOGTAIL_SOURCE_TOKEN"
LOGTAIL_URL = "https://in.logs.betterstack.com/"


def _build_payload(message, level, service, **fields):
    payload = {
        "dt": datetime.now(timezone.utc).isoformat(),
        "message": message,
        "level": level,
        "service": service,
    }
    payload.update(fields)
    return payload


def write_structured_log(message, level="info", service="application", **fields):
    token = os.environ.get(LOGTAIL_SOURCE_TOKEN_ENV)
    if not token:
        raise ValueError(f"Missing required environment variable: {LOGTAIL_SOURCE_TOKEN_ENV}")

    payload = _build_payload(message, level, service, **fields)
    response = requests.post(
        LOGTAIL_URL,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
        },
        data=json.dumps(payload),
        timeout=15,
    )
    response.raise_for_status()
    return response.json() if response.content else None


__all__ = ["write_structured_log"]
