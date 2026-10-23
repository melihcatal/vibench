import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import requests


DATABRICKS_HOST = os.getenv("DATABRICKS_HOST", "").rstrip("/")
DATABRICKS_TOKEN = os.getenv("DATABRICKS_TOKEN", "")
DEFAULT_METRIC_QUERY = os.getenv("DATABRICKS_METRIC_QUERY", "")


def _iso_z(dt: datetime) -> str:
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def aggregate_metric_stats(
    metric_query: Optional[str] = None,
    start_time: Optional[datetime] = None,
    end_time: Optional[datetime] = None,
    aggregation: str = "avg",
    step_seconds: int = 300,
) -> Dict[str, Any]:
    if not DATABRICKS_HOST:
        raise ValueError("DATABRICKS_HOST is required")
    if not DATABRICKS_TOKEN:
        raise ValueError("DATABRICKS_TOKEN is required")

    metric_query = metric_query or DEFAULT_METRIC_QUERY
    if not metric_query:
        raise ValueError("metric_query is required")

    end_time = end_time or datetime.now(timezone.utc)
    start_time = start_time or (end_time - timedelta(hours=1))

    url = f"{DATABRICKS_HOST}/api/2.0/metrics/query"
    headers = {
        "Authorization": f"Bearer {DATABRICKS_TOKEN}",
        "Content-Type": "application/json",
    }
    payload = {
        "query": metric_query,
        "start_time": _iso_z(start_time),
        "end_time": _iso_z(end_time),
        "aggregation": aggregation,
        "step_seconds": step_seconds,
    }
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()

    series = data.get("series", [])
    values = []
    for item in series:
        points = item.get("points", [])
        for point in points:
            value = point.get("value")
            if isinstance(value, (int, float)):
                values.append(float(value))

    summary = {
        "metric_query": metric_query,
        "start_time": _iso_z(start_time),
        "end_time": _iso_z(end_time),
        "aggregation": aggregation,
        "step_seconds": step_seconds,
        "points": len(values),
        "min": min(values) if values else None,
        "max": max(values) if values else None,
        "sum": sum(values) if values else None,
        "avg": (sum(values) / len(values)) if values else None,
        "raw": data,
    }
    return summary


if __name__ == "__main__":
    import json
    import sys

    query = sys.argv[1] if len(sys.argv) > 1 else None
    result = aggregate_metric_stats(metric_query=query)
    print(json.dumps(result, indent=2, sort_keys=True))
