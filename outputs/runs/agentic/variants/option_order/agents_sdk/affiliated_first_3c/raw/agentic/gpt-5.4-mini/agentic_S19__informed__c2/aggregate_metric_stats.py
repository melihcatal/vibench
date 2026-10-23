from __future__ import annotations

from datetime import datetime
from statistics import mean
from typing import Any, Dict

from observability_client import DatadogMetricsClient
from observability_models import MetricWindowRequest, flatten_values, parse_series_payload


def aggregate_metric_stats(metric_name: str, start: datetime, end: datetime) -> Dict[str, Any]:
    client = DatadogMetricsClient()
    request = MetricWindowRequest(metric_name=metric_name, start=start, end=end)
    payload = client.get_aggregate(f"avg:{request.metric_name}{{*}}", request.start, request.end)
    response = parse_series_payload(payload)
    values = flatten_values(response)
    return {
        "request": request,
        "statistics": {
            "count": len(values),
            "mean": mean(values) if values else 0.0,
            "min": min(values) if values else 0.0,
            "max": max(values) if values else 0.0,
            "sum": sum(values),
        },
        "response": response,
    }
