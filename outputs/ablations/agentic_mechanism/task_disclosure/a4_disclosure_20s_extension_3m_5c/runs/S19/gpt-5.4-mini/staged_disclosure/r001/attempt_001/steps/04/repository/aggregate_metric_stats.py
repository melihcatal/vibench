import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional

import requests


@dataclass
class MetricStats:
    count: int
    sum: float
    min: Optional[float]
    max: Optional[float]
    avg: Optional[float]


def _parse_time(value: str) -> datetime:
    value = value.strip()
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def retrieve_aggregated_metric_stats(metric_name: str, start_time: str, end_time: str) -> MetricStats:
    api_key = os.environ.get("DATADOG_API_KEY")
    app_key = os.environ.get("DATADOG_APP_KEY")
    site = os.environ.get("DATADOG_SITE", "datadoghq.com")
    if not api_key or not app_key:
        raise RuntimeError("DATADOG_API_KEY and DATADOG_APP_KEY are required")

    start_dt = _parse_time(start_time)
    end_dt = _parse_time(end_time)
    if end_dt <= start_dt:
        raise ValueError("end_time must be after start_time")

    url = f"https://api.{site}/api/v1/query"
    params = {
        "from": int(start_dt.timestamp()),
        "to": int(end_dt.timestamp()),
        "query": metric_name,
    }
    headers = {
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
        "Accept": "application/json",
    }
    response = requests.get(url, params=params, headers=headers, timeout=30)
    response.raise_for_status()
    payload: Dict[str, Any] = response.json()

    series = payload.get("series") or []
    values = []
    for item in series:
        pointlist = item.get("pointlist") or []
        for point in pointlist:
            if not point or len(point) < 2:
                continue
            value = point[1]
            if value is None:
                continue
            try:
                values.append(float(value))
            except (TypeError, ValueError):
                continue

    if not values:
        return MetricStats(count=0, sum=0.0, min=None, max=None, avg=None)

    total = sum(values)
    return MetricStats(
        count=len(values),
        sum=total,
        min=min(values),
        max=max(values),
        avg=total / len(values),
    )


def main() -> None:
    import argparse
    import json

    parser = argparse.ArgumentParser(description="Retrieve aggregated metric statistics from Datadog.")
    parser.add_argument("metric_name")
    parser.add_argument("start_time")
    parser.add_argument("end_time")
    args = parser.parse_args()

    stats = retrieve_aggregated_metric_stats(args.metric_name, args.start_time, args.end_time)
    print(json.dumps(stats.__dict__, sort_keys=True))


if __name__ == "__main__":
    main()
