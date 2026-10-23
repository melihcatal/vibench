import os
import sys
from datetime import datetime, timedelta, timezone

import requests


def _parse_iso8601(value: str) -> datetime:
    value = value.strip()
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value)


def _default_window_minutes() -> int:
    raw = os.getenv("LOGTAIL_WINDOW_MINUTES", "60")
    try:
        return max(1, int(raw))
    except ValueError:
        return 60


def _build_query(severity: str, start: datetime, end: datetime) -> dict:
    query = (
        f'severity:{severity} AND timestamp:["{start.astimezone(timezone.utc).isoformat()}" '
        f'TO "{end.astimezone(timezone.utc).isoformat()}"]'
    )
    return {
        "query": query,
        "from": start.astimezone(timezone.utc).isoformat(),
        "to": end.astimezone(timezone.utc).isoformat(),
        "limit": 100,
    }


def fetch_error_logs(severity: str, start: datetime, end: datetime):
    api_key = os.getenv("LOGTAIL_SOURCE_TOKEN")
    source_token = os.getenv("LOGTAIL_LOG_SOURCE_TOKEN")
    if not api_key or not source_token:
        raise RuntimeError("LOGTAIL_SOURCE_TOKEN and LOGTAIL_LOG_SOURCE_TOKEN are required")

    url = f"https://api.logtail.com/v1/sources/{source_token}/search"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    response = requests.post(url, headers=headers, json=_build_query(severity, start, end), timeout=30)
    response.raise_for_status()
    payload = response.json()
    return payload.get("data", payload)


def main() -> int:
    severity = sys.argv[1] if len(sys.argv) > 1 else os.getenv("LOG_SEVERITY", "error")
    end = datetime.now(timezone.utc)
    window_minutes = _default_window_minutes()
    start = end - timedelta(minutes=window_minutes)

    if len(sys.argv) > 2:
        start = _parse_iso8601(sys.argv[2])
    if len(sys.argv) > 3:
        end = _parse_iso8601(sys.argv[3])

    logs = fetch_error_logs(severity, start, end)
    if isinstance(logs, list):
        for entry in logs:
            print(entry)
    else:
        print(logs)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
