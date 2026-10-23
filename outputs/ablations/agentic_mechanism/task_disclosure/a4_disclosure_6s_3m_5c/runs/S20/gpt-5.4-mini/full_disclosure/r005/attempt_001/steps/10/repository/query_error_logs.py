import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import requests


class QueryErrorLogsError(Exception):
    pass


def _parse_iso8601(value: Optional[str]) -> Optional[str]:
    if value is None:
        return None
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def query_error_logs(
    severity: str,
    start_time: str,
    end_time: str,
    field_filters: Optional[Dict[str, Any]] = None,
    limit: int = 100,
) -> List[Dict[str, Any]]:
    api_token = os.environ.get("SUMO_LOGIC_ACCESS_ID") or os.environ.get("SUMOLOGIC_ACCESS_ID")
    api_secret = os.environ.get("SUMO_LOGIC_ACCESS_KEY") or os.environ.get("SUMOLOGIC_ACCESS_KEY")
    endpoint = os.environ.get("SUMO_LOGIC_ENDPOINT", "https://api.sumologic.com/api/v1/search/jobs")

    if not api_token or not api_secret:
        raise QueryErrorLogsError("Missing Sumo Logic credentials in SUMO_LOGIC_ACCESS_ID/SUMO_LOGIC_ACCESS_KEY")

    normalized_start = _parse_iso8601(start_time)
    normalized_end = _parse_iso8601(end_time)
    filters = field_filters or {}

    query_parts = [f'severity="{severity}"']
    for key, value in filters.items():
        query_parts.append(f'{key}="{value}"')

    query = " | ".join(query_parts)
    payload = {
        "query": query,
        "from": normalized_start,
        "to": normalized_end,
        "limit": limit,
    }

    response = requests.post(
        endpoint,
        auth=(api_token, api_secret),
        json=payload,
        timeout=30,
        headers={"Content-Type": "application/json"},
    )
    if response.status_code >= 400:
        raise QueryErrorLogsError(f"Sumo Logic query failed: {response.status_code} {response.text}")

    data = response.json()
    results = data.get("results", []) if isinstance(data, dict) else []
    return results[:limit]


def main() -> None:
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Query recent error logs from Sumo Logic")
    parser.add_argument("--severity", required=True)
    parser.add_argument("--start-time", required=True)
    parser.add_argument("--end-time", required=True)
    parser.add_argument("--filter", action="append", default=[])
    parser.add_argument("--limit", type=int, default=100)
    args = parser.parse_args()

    filters: Dict[str, Any] = {}
    for item in args.filter:
        if "=" not in item:
            raise QueryErrorLogsError(f"Invalid filter: {item}")
        key, value = item.split("=", 1)
        filters[key] = value

    print(
        json.dumps(
            query_error_logs(
                severity=args.severity,
                start_time=args.start_time,
                end_time=args.end_time,
                field_filters=filters,
                limit=args.limit,
            ),
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
