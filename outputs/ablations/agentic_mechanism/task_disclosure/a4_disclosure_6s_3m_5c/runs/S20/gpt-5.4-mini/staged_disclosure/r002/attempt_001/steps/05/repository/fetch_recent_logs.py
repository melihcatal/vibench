import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import requests


SPLUNK_API_BASE_URL = os.environ.get("SPLUNK_API_BASE_URL", "https://api.splunk.com")
SPLUNK_TOKEN = os.environ.get("SPLUNK_TOKEN", "")


def _isoformat_utc(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def fetch_recent_logs(
    field_filters: Dict[str, Any],
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    limit: int = 100,
) -> List[Dict[str, Any]]:
    if not SPLUNK_TOKEN:
        raise ValueError("SPLUNK_TOKEN is required")

    if end_time is None:
        end_time = datetime.now(timezone.utc)
    if start_time is None:
        start_time = end_time - timedelta(hours=1)

    query_parts = [f"{k}=\"{v}\"" for k, v in field_filters.items()]
    query = " AND ".join(query_parts) if query_parts else "*"

    params = {
        "query": query,
        "start_time": _isoformat_utc(start_time),
        "end_time": _isoformat_utc(end_time),
        "limit": limit,
    }

    response = requests.get(
        f"{SPLUNK_API_BASE_URL.rstrip('/')}/v1/search/logs",
        headers={"Authorization": f"Bearer {SPLUNK_TOKEN}"},
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    if isinstance(data, dict) and "results" in data:
        return data["results"]
    if isinstance(data, list):
        return data
    return []


if __name__ == "__main__":
    logs = fetch_recent_logs({"service": "api", "level": "error"})
    print(logs)
