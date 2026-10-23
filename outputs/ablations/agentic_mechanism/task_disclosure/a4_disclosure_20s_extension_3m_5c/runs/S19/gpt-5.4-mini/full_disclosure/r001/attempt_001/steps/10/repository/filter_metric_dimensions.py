import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import requests


@dataclass
class FilterMetricDimensionsRequest:
    metric_name: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    dimensions: Optional[Dict[str, str]] = None
    labels: Optional[Dict[str, str]] = None
    limit: int = 100


def _iso(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _build_filter_expression(dimensions: Optional[Dict[str, str]], labels: Optional[Dict[str, str]]) -> str:
    clauses: List[str] = []
    for source in (dimensions or {}, labels or {}):
        for key, value in source.items():
            safe_key = key.replace('"', '\\"')
            safe_value = value.replace('"', '\\"')
            clauses.append(f'{safe_key} = "{safe_value}"')
    return " AND ".join(clauses)


def query_metric_dimensions(request: FilterMetricDimensionsRequest) -> Dict[str, Any]:
    api_key = os.environ.get("DATADOG_API_KEY")
    app_key = os.environ.get("DATADOG_APP_KEY")
    if not api_key or not app_key:
        raise ValueError("DATADOG_API_KEY and DATADOG_APP_KEY are required")

    end_time = request.end_time or datetime.now(timezone.utc)
    start_time = request.start_time or (end_time - timedelta(hours=1))
    filter_expression = _build_filter_expression(request.dimensions, request.labels)
    query = request.metric_name if not filter_expression else f"{request.metric_name}{{{filter_expression}}}"

    params = {
        "from": int(start_time.timestamp()),
        "to": int(end_time.timestamp()),
        "query": query,
        "page[size]": request.limit,
    }
    response = requests.get(
        "https://api.datadoghq.com/api/v1/query",
        headers={
            "DD-API-KEY": api_key,
            "DD-APPLICATION-KEY": app_key,
        },
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    return {
        "metric_name": request.metric_name,
        "query": query,
        "start_time": _iso(start_time),
        "end_time": _iso(end_time),
        "series": payload.get("series", []),
        "raw": payload,
    }


def main() -> None:
    metric = os.environ.get("METRIC_NAME", "system.cpu.user")
    request = FilterMetricDimensionsRequest(metric_name=metric)
    result = query_metric_dimensions(request)
    print(result)


if __name__ == "__main__":
    main()
