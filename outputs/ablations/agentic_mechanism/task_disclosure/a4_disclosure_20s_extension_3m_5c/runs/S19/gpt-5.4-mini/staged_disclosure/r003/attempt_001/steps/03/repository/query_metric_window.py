import os
import sys
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import requests


DATADOG_API_BASE = "https://api.datadoghq.com"


def _parse_time(value: Optional[str], default: datetime) -> datetime:
    if not value:
        return default
    if value.isdigit():
        return datetime.fromtimestamp(int(value), tz=timezone.utc)
    normalized = value.replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def query_metric_window(metric_name: str, start_time: datetime, end_time: datetime, interval: int = 300) -> Dict[str, Any]:
    api_key = os.environ.get("DD_API_KEY")
    app_key = os.environ.get("DD_APP_KEY")
    if not api_key or not app_key:
        raise RuntimeError("DD_API_KEY and DD_APP_KEY must be set")

    params = {
        "from": int(start_time.timestamp()),
        "to": int(end_time.timestamp()),
        "query": metric_name,
        "interval": interval,
    }
    headers = {
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
    }
    response = requests.get(f"{DATADOG_API_BASE}/api/v1/query", params=params, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()


def main() -> int:
    if len(sys.argv) < 2:
        raise SystemExit("usage: query_metric_window.py METRIC_NAME [WINDOW_MINUTES] [END_TIME]")

    metric_name = sys.argv[1]
    window_minutes = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    end_time = _parse_time(sys.argv[3] if len(sys.argv) > 3 else None, datetime.now(timezone.utc))
    start_time = end_time - timedelta(minutes=window_minutes)

    result = query_metric_window(metric_name, start_time, end_time)
    print(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
