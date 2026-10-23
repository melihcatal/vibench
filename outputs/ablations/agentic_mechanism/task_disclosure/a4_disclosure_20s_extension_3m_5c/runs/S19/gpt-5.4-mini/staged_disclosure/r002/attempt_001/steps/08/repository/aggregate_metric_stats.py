import argparse
import os
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import requests


DD_API_HOST = "https://api.datadoghq.com"


def _parse_time(value: str) -> int:
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return int(dt.timestamp())
    except ValueError as exc:
        raise SystemExit(f"Invalid time value: {value}") from exc


def aggregate_metric_stats(metric: str, start: int, end: int, interval: int = 300) -> Dict[str, Any]:
    api_key = os.environ.get("DATADOG_API_KEY")
    app_key = os.environ.get("DATADOG_APP_KEY")
    if not api_key or not app_key:
        raise SystemExit("DATADOG_API_KEY and DATADOG_APP_KEY must be set")

    url = f"{DD_API_HOST}/api/v1/query"
    params = {"from": start, "to": end, "query": metric}
    headers = {
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
        "Accept": "application/json",
    }
    response = requests.get(url, params=params, headers=headers, timeout=30)
    response.raise_for_status()
    payload = response.json()

    series = payload.get("series", []) or []
    values = []
    for item in series:
        for point in item.get("pointlist", []) or []:
            if len(point) >= 2 and point[1] is not None:
                values.append(float(point[1]))

    if not values:
        return {
            "metric": metric,
            "start": start,
            "end": end,
            "interval": interval,
            "count": 0,
            "min": None,
            "max": None,
            "avg": None,
            "sum": 0.0,
        }

    total = sum(values)
    return {
        "metric": metric,
        "start": start,
        "end": end,
        "interval": interval,
        "count": len(values),
        "min": min(values),
        "max": max(values),
        "avg": total / len(values),
        "sum": total,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Retrieve aggregated Datadog metric statistics over a time window")
    parser.add_argument("metric")
    parser.add_argument("--start", required=True, help="ISO-8601 datetime or unix timestamp")
    parser.add_argument("--end", required=True, help="ISO-8601 datetime or unix timestamp")
    parser.add_argument("--interval", type=int, default=300)
    args = parser.parse_args()

    start = int(args.start) if args.start.isdigit() else _parse_time(args.start)
    end = int(args.end) if args.end.isdigit() else _parse_time(args.end)
    stats = aggregate_metric_stats(args.metric, start, end, args.interval)
    print(stats)


if __name__ == "__main__":
    main()
