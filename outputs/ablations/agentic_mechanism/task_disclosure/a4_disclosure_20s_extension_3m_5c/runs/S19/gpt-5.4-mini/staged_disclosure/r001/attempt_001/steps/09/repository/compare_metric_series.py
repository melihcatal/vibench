import argparse
import json
import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import requests


OPENMETRICS_API_BASE = "https://api.datadoghq.com"


def _parse_time(value: str) -> int:
    if value.isdigit():
        return int(value)
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp())


def _query_datadog(series_query: str, start: int, end: int) -> Dict[str, Any]:
    api_key = os.getenv("DD_API_KEY")
    app_key = os.getenv("DD_APP_KEY")
    if not api_key or not app_key:
        raise RuntimeError("DD_API_KEY and DD_APP_KEY are required")
    url = f"{OPENMETRICS_API_BASE}/api/v1/query"
    resp = requests.get(
        url,
        params={"from": start, "to": end, "query": series_query},
        headers={"DD-API-KEY": api_key, "DD-APPLICATION-KEY": app_key},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def _normalize_points(payload: Dict[str, Any]) -> List[Tuple[int, float]]:
    results = payload.get("series", [])
    if not results:
        return []
    points = results[0].get("pointlist", [])
    normalized: List[Tuple[int, float]] = []
    for ts_ms, val in points:
        if val is None:
            continue
        normalized.append((int(ts_ms // 1000), float(val)))
    return normalized


def _summary(points: List[Tuple[int, float]]) -> Dict[str, Optional[float]]:
    values = [v for _, v in points]
    if not values:
        return {"count": 0, "min": None, "max": None, "avg": None, "last": None}
    return {
        "count": len(values),
        "min": min(values),
        "max": max(values),
        "avg": sum(values) / len(values),
        "last": values[-1],
    }


def compare_metric_series(metric: str, series_a: str, series_b: str, start: int, end: int) -> Dict[str, Any]:
    query_a = f"{metric}{{{series_a}}}"
    query_b = f"{metric}{{{series_b}}}"
    payload_a = _query_datadog(query_a, start, end)
    payload_b = _query_datadog(query_b, start, end)
    points_a = _normalize_points(payload_a)
    points_b = _normalize_points(payload_b)
    summary_a = _summary(points_a)
    summary_b = _summary(points_b)
    return {
        "provider": "datadog",
        "metric": metric,
        "window": {"start": start, "end": end},
        "series": {
            "a": {"filter": series_a, "summary": summary_a, "points": points_a},
            "b": {"filter": series_b, "summary": summary_b, "points": points_b},
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare Datadog metric series over the same window.")
    parser.add_argument("--metric", required=True)
    parser.add_argument("--series-a", required=True)
    parser.add_argument("--series-b", required=True)
    parser.add_argument("--start", required=True)
    parser.add_argument("--end", required=True)
    args = parser.parse_args()

    result = compare_metric_series(
        metric=args.metric,
        series_a=args.series_a,
        series_b=args.series_b,
        start=_parse_time(args.start),
        end=_parse_time(args.end),
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
