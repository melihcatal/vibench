import argparse
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import requests


DATADOG_API_HOST = "https://api.datadoghq.com"
DATADOG_SERIES_QUERY = "/api/v1/query"


@dataclass
class MetricSeries:
    scope: str
    points: List[Tuple[int, float]]


def _build_query(metric: str, filter_expr: Optional[str], aggregator: str) -> str:
    if filter_expr:
        return f"{aggregator}:{metric}{{{filter_expr}}}"
    return f"{aggregator}:{metric}{{*}}"


def _fetch_datadog_series(metric: str, filter_expr: Optional[str], start: int, end: int, step: int, aggregator: str) -> MetricSeries:
    api_key = os.environ.get("DATADOG_API_KEY")
    app_key = os.environ.get("DATADOG_APP_KEY")
    if not api_key or not app_key:
        raise RuntimeError("DATADOG_API_KEY and DATADOG_APP_KEY are required")

    query = _build_query(metric, filter_expr, aggregator)
    resp = requests.get(
        f"{DATADOG_API_HOST}{DATADOG_SERIES_QUERY}",
        params={"from": start, "to": end, "query": query, "step": step},
        headers={"DD-API-KEY": api_key, "DD-APPLICATION-KEY": app_key},
        timeout=30,
    )
    resp.raise_for_status()
    payload: Dict[str, Any] = resp.json()
    series = payload.get("series", [])
    if not series:
        return MetricSeries(scope=filter_expr or "all", points=[])

    first = series[0]
    points = [(int(ts), float(val)) for ts, val in first.get("pointlist", []) if ts is not None and val is not None]
    return MetricSeries(scope=filter_expr or "all", points=points)


def _summarize_difference(left: MetricSeries, right: MetricSeries) -> Dict[str, Any]:
    left_map = dict(left.points)
    right_map = dict(right.points)
    common = sorted(set(left_map) & set(right_map))
    deltas = [left_map[ts] - right_map[ts] for ts in common]
    if not deltas:
        return {"shared_points": 0, "mean_delta": None, "max_delta": None, "min_delta": None}
    return {
        "shared_points": len(common),
        "mean_delta": sum(deltas) / len(deltas),
        "max_delta": max(deltas),
        "min_delta": min(deltas),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare Datadog metric series across two resource filters")
    parser.add_argument("metric")
    parser.add_argument("left_filter")
    parser.add_argument("right_filter")
    parser.add_argument("--start", type=int, required=True)
    parser.add_argument("--end", type=int, required=True)
    parser.add_argument("--step", type=int, default=60)
    parser.add_argument("--aggregator", default="avg")
    args = parser.parse_args()

    left = _fetch_datadog_series(args.metric, args.left_filter, args.start, args.end, args.step, args.aggregator)
    right = _fetch_datadog_series(args.metric, args.right_filter, args.start, args.end, args.step, args.aggregator)
    result = {
        "metric": args.metric,
        "left_scope": left.scope,
        "right_scope": right.scope,
        "comparison": _summarize_difference(left, right),
    }
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
