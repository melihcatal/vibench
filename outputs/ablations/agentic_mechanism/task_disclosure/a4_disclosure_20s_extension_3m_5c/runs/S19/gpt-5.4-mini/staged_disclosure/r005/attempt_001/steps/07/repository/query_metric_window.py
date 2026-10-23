import argparse
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import requests


PROMETHEUS_URL = os.environ.get("PROMETHEUS_URL", "http://localhost:9090")


def parse_duration(value: str) -> timedelta:
    units = {
        "s": 1,
        "m": 60,
        "h": 3600,
        "d": 86400,
        "w": 604800,
    }
    if not value:
        raise ValueError("duration is required")
    suffix = value[-1]
    if suffix not in units:
        raise ValueError("duration must end with s, m, h, d, or w")
    amount = float(value[:-1])
    return timedelta(seconds=amount * units[suffix])


def prometheus_query_range(metric: str, start: datetime, end: datetime, step: str) -> Dict[str, Any]:
    url = f"{PROMETHEUS_URL.rstrip('/')}/api/v1/query_range"
    params = {
        "query": metric,
        "start": start.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        "end": end.astimezone(timezone.utc).isoformat().replace("+00:00", "Z"),
        "step": step,
    }
    response = requests.get(url, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()
    if payload.get("status") != "success":
        raise RuntimeError(f"Prometheus query failed: {payload}")
    return payload


def extract_datapoints(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    for series in payload.get("data", {}).get("result", []):
        metric_labels = series.get("metric", {})
        for ts, value in series.get("values", []):
            results.append(
                {
                    "timestamp": datetime.fromtimestamp(float(ts), tz=timezone.utc).isoformat(),
                    "value": float(value),
                    "labels": metric_labels,
                }
            )
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Query recent datapoints for a metric from Prometheus.")
    parser.add_argument("metric", help="PromQL metric or expression")
    parser.add_argument("--window", default="1h", help="Lookback window, e.g. 15m, 1h, 1d")
    parser.add_argument("--step", default="60s", help="Query step, e.g. 15s, 60s, 5m")
    args = parser.parse_args()

    end = datetime.now(timezone.utc)
    start = end - parse_duration(args.window)
    payload = prometheus_query_range(args.metric, start, end, args.step)
    datapoints = extract_datapoints(payload)
    for point in datapoints:
        print(f"{point['timestamp']}\t{point['value']}\t{point['labels']}")


if __name__ == "__main__":
    main()
