import os
from datetime import datetime, timedelta, timezone

import requests


BETTERSTACK_API_BASE = "https://api.betterstack.com"


def _api_token() -> str:
    token = os.getenv("BETTERSTACK_API_TOKEN") or os.getenv("LOGTAIL_API_KEY")
    if not token:
        raise RuntimeError("Missing BETTERSTACK_API_TOKEN or LOGTAIL_API_KEY")
    return token


def _source_id() -> str:
    source_id = os.getenv("BETTERSTACK_SOURCE_ID") or os.getenv("LOGTAIL_SOURCE_ID")
    if not source_id:
        raise RuntimeError("Missing BETTERSTACK_SOURCE_ID or LOGTAIL_SOURCE_ID")
    return source_id


def _parse_time(value: str | None, fallback: datetime) -> datetime:
    if not value:
        return fallback
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def query_error_logs(severity: str = "error", start_time: str | None = None, end_time: str | None = None, limit: int = 100):
    end_dt = _parse_time(end_time, datetime.now(timezone.utc))
    start_dt = _parse_time(start_time, end_dt - timedelta(hours=24))
    response = requests.get(
        f"{BETTERSTACK_API_BASE}/v1/sources/{_source_id()}/query",
        headers={"Authorization": f"Bearer {_api_token()}"},
        params={
            "query": f'severity:"{severity}"',
            "start_dt": start_dt.isoformat(),
            "end_dt": end_dt.isoformat(),
            "limit": limit,
        },
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    return data.get("data", data)


if __name__ == "__main__":
    import json
    import sys

    severity = sys.argv[1] if len(sys.argv) > 1 else "error"
    start_time = sys.argv[2] if len(sys.argv) > 2 else None
    end_time = sys.argv[3] if len(sys.argv) > 3 else None
    print(json.dumps(query_error_logs(severity=severity, start_time=start_time, end_time=end_time), indent=2))
