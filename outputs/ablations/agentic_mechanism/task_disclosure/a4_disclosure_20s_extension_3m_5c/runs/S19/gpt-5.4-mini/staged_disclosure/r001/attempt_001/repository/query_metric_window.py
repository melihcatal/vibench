import argparse
import json
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import requests


PROMETHEUS_API_URL = os.getenv("PROMETHEUS_API_URL", "https://prometheus.example.com")
PROMETHEUS_TOKEN = os.getenv("PROMETHEUS_TOKEN")


def parse_time(value: Optional[str]) -> datetime:
    if value is None:
        return datetime.now(timezone.utc)
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise SystemExit(f"invalid time: {value}") from exc
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def build_query(metric: str, start: datetime, end: datetime, step_seconds: int) -> Dict[str, Any]:
    url = f"{PROMETHEUS_API_URL.rstrip('/')}/api/v1/query_range"
    headers = {"Accept": "application/json"}
    if PROMETHEUS_TOKEN:
        headers["Authorization"] = f"Bearer {PROMETHEUS_TOKEN}"
    params = {
        "query": metric,
        "start": start.isoformat(),
        "end": end.isoformat(),
        "step": str(step_seconds),
    }
    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()
    if payload.get("status") != "success":
        raise SystemExit(json.dumps(payload))
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Query recent datapoints for a metric from Prometheus.")
    parser.add_argument("metric", help="Prometheus metric name or query")
    parser.add_argument("--window", default="15m", help="Lookback window, e.g. 15m, 1h, 2d")
    parser.add_argument("--step", type=int, default=60, help="Query step in seconds")
    parser.add_argument("--end", default=None, help="End time in RFC3339 format")
    args = parser.parse_args()

    now = parse_time(args.end)
    unit = args.window[-1]
    amount = int(args.window[:-1])
    delta = {
        "m": timedelta(minutes=amount),
        "h": timedelta(hours=amount),
        "d": timedelta(days=amount),
        "s": timedelta(seconds=amount),
    }.get(unit)
    if delta is None:
        raise SystemExit("window must end with s, m, h, or d")
    start = now - delta

    payload = build_query(args.metric, start, now, args.step)
    results: List[Dict[str, Any]] = payload.get("data", {}).get("result", [])
    print(json.dumps(results, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
