import json
import os
from datetime import datetime, timezone

import requests


def write_structured_log(message: str, level: str = "info", **fields):
    api_key = os.environ["LOGTAIL_SOURCE_TOKEN"]
    source_token = os.environ.get("LOGTAIL_SOURCE_TOKEN")
    if not source_token:
        raise RuntimeError("LOGTAIL_SOURCE_TOKEN is required")

    payload = {
        "dt": datetime.now(timezone.utc).isoformat(),
        "level": level,
        "message": message,
        **fields,
    }

    response = requests.post(
        "https://in.logs.betterstack.com",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        data=json.dumps(payload),
        timeout=10,
    )
    response.raise_for_status()
    return response.json() if response.content else None
