import json
import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import requests


@dataclass
class LogQueryResult:
    records: List[Dict[str, Any]]
    next_page_token: Optional[str] = None


def _parse_time(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def fetch_recent_logs(
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    field_filters: Optional[Dict[str, Any]] = None,
    limit: int = 100,
) -> LogQueryResult:
    api_key = os.environ["SENTRY_AUTH_TOKEN"]
    org_slug = os.environ["SENTRY_ORG_SLUG"]
    project_slug = os.environ["SENTRY_PROJECT_SLUG"]
    url = f"https://sentry.io/api/0/projects/{org_slug}/{project_slug}/events/"
    headers = {"Authorization": f"Bearer {api_key}", "Accept": "application/json"}
    params: Dict[str, Any] = {"limit": limit}
    query_parts = []
    if start_time:
        query_parts.append(f"timestamp:>{_parse_time(start_time)}")
    if end_time:
        query_parts.append(f"timestamp:<{_parse_time(end_time)}")
    if field_filters:
        for key, value in field_filters.items():
            query_parts.append(f'{key}:{json.dumps(value).strip("\"")}')
    if query_parts:
        params["query"] = " ".join(query_parts)
    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()
    if isinstance(payload, list):
        records = payload
    elif isinstance(payload, dict) and "data" in payload:
        records = payload["data"]
    else:
        records = [payload]
    return LogQueryResult(records=records, next_page_token=None)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--start-time")
    parser.add_argument("--end-time")
    parser.add_argument("--field-filter", action="append", default=[])
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()
    field_filters: Dict[str, Any] = {}
    for item in args.field_filter:
        if "=" not in item:
            raise ValueError("field filters must be in key=value format")
        key, value = item.split("=", 1)
        field_filters[key] = value
    result = fetch_recent_logs(args.start_time, args.end_time, field_filters or None, args.limit)
    print(json.dumps({"records": result.records, "next_page_token": result.next_page_token}))


if __name__ == "__main__":
    main()
