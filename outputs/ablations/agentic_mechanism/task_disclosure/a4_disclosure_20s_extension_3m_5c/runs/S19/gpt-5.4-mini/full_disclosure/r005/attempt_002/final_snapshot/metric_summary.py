import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import requests


def _to_float(value: Any) -> Optional[float]:
    try:
        if value is None:
            return None
        return float(value)
    except (TypeError, ValueError):
        return None


def _parse_points(payload: Dict[str, Any]) -> List[float]:
    points: List[float] = []
    for item in payload.get("data", []):
        value = item.get("value")
        if isinstance(value, dict):
            value = value.get("avg") or value.get("sum") or value.get("last")
        numeric = _to_float(value)
        if numeric is not None:
            points.append(numeric)
    return points


def _trend_summary(points: List[float]) -> Dict[str, Any]:
    if not points:
        return {"trend": "no data", "anomaly": False, "message": "No datapoints returned."}

    first = points[0]
    last = points[-1]
    minimum = min(points)
    maximum = max(points)
    average = sum(points) / len(points)

    if len(points) >= 4:
        baseline = sum(points[:-1]) / (len(points) - 1)
    else:
        baseline = average

    delta = last - first
    pct_change = None if first == 0 else (delta / abs(first)) * 100.0
    deviation = None if baseline == 0 else abs(last - baseline) / abs(baseline) * 100.0
    anomaly = bool(deviation is not None and deviation >= 30.0)

    if delta > 0:
        trend = "rising"
    elif delta < 0:
        trend = "falling"
    else:
        trend = "flat"

    return {
        "trend": trend,
        "anomaly": anomaly,
        "points": len(points),
        "first": first,
        "last": last,
        "min": minimum,
        "max": maximum,
        "average": average,
        "change_percent": pct_change,
        "deviation_from_baseline_percent": deviation,
    }


def summarize_metric(metric_name: str, window_minutes: int = 60) -> Dict[str, Any]:
    api_key = os.environ.get("DATADOG_API_KEY")
    app_key = os.environ.get("DATADOG_APP_KEY")
    site = os.environ.get("DATADOG_SITE", "datadoghq.com")
    if not api_key or not app_key:
        raise RuntimeError("DATADOG_API_KEY and DATADOG_APP_KEY are required")

    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=window_minutes)
    url = f"https://api.{site}/api/v1/query"
    params = {
        "from": int(start.timestamp()),
        "to": int(end.timestamp()),
        "query": metric_name,
    }
    headers = {
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
        "Accept": "application/json",
    }
    response = requests.get(url, params=params, headers=headers, timeout=30)
    response.raise_for_status()
    payload = response.json()
    points = _parse_points(payload)
    summary = _trend_summary(points)
    summary.update(
        {
            "metric_name": metric_name,
            "window_minutes": window_minutes,
            "provider": "Datadog",
            "start": start.isoformat(),
            "end": end.isoformat(),
        }
    )
    return summary


if __name__ == "__main__":
    import json
    import sys

    metric = sys.argv[1] if len(sys.argv) > 1 else "avg:system.cpu.user{*}"
    minutes = int(sys.argv[2]) if len(sys.argv) > 2 else 60
    print(json.dumps(summarize_metric(metric, minutes), indent=2, sort_keys=True))
