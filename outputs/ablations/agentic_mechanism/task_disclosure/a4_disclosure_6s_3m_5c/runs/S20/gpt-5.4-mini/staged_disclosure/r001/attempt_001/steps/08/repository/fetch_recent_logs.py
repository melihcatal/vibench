import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import requests


def _to_iso8601(value: str) -> str:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def fetch_recent_logs(
    field_filters: Dict[str, Any],
    start_time: str,
    end_time: str,
    limit: int = 100,
) -> List[Dict[str, Any]]:
    api_key = os.environ.get("SPLUNK_HEC_TOKEN")
    base_url = os.environ.get("SPLUNK_SEARCH_API_URL", "https://api.splunk.com")
    if not api_key:
        raise RuntimeError("SPLUNK_HEC_TOKEN is required")

    query_parts = [f'{field}="{value}"' for field, value in field_filters.items()]
    query = " AND ".join(query_parts) if query_parts else "*"
    payload = {
        "search": f"search {query} earliest={_to_iso8601(start_time)} latest={_to_iso8601(end_time)} | head {int(limit)}",
        "output_mode": "json",
    }
    response = requests.post(
        f"{base_url.rstrip('/')}/services/search/jobs/export",
        headers={"Authorization": f"Bearer {api_key}"},
        data=payload,
        timeout=30,
    )
    response.raise_for_status()

    logs: List[Dict[str, Any]] = []
    for line in response.text.splitlines():
        if not line.strip():
            continue
        item = json.loads(line)
        if isinstance(item, dict):
            logs.append(item)
    return logs


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--field", action="append", default=[])
    parser.add_argument("--start-time", required=True)
    parser.add_argument("--end-time", required=True)
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()

    filters: Dict[str, Any] = {}
    for item in args.field:
        if "=" not in item:
            raise ValueError("Field filters must be provided as key=value")
        key, value = item.split("=", 1)
        filters[key] = value

    print(json.dumps(fetch_recent_logs(filters, args.start_time, args.end_time, args.limit), indent=2))
