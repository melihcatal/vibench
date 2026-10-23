import os
import time
from typing import Any, Dict, List, Optional

import requests


LOGTAIL_BASE_URL = "https://api.logtail.com"


def fetch_recent_logs(field_filters: Dict[str, Any], start_time: float, end_time: float, limit: int = 100) -> List[Dict[str, Any]]:
    source_token = os.environ.get("LOGTAIL_SOURCE_TOKEN")
    api_token = os.environ.get("LOGTAIL_API_TOKEN")
    if not source_token or not api_token:
        raise RuntimeError("LOGTAIL_SOURCE_TOKEN and LOGTAIL_API_TOKEN are required")

    params: Dict[str, Any] = {
        "start": int(start_time),
        "end": int(end_time),
        "limit": limit,
    }
    for key, value in field_filters.items():
        params[key] = value

    response = requests.get(
        f"{LOGTAIL_BASE_URL}/sources/{source_token}/logs",
        headers={"Authorization": f"Bearer {api_token}"},
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    if isinstance(payload, dict):
        return payload.get("data", payload.get("logs", []))
    return payload


if __name__ == "__main__":
    now = time.time()
    logs = fetch_recent_logs({}, now - 3600, now)
    print(logs)
