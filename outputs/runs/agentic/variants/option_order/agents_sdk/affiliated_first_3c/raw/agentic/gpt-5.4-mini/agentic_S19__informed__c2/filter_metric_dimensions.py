from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from observability_client import DatadogMetricsClient
from observability_models import MetricFilterRequest, parse_series_payload, to_query


def filter_metric_dimensions(metric_name: str, start: datetime, end: datetime, filters: Dict[str, str]) -> Dict[str, Any]:
    client = DatadogMetricsClient()
    request = MetricFilterRequest(metric_name=metric_name, start=start, end=end, filters=filters)
    query = f"avg:{request.metric_name}{to_query(request.filters)}"
    payload = client.query(query, request.start, request.end)
    return {"request": request, "response": parse_series_payload(payload)}
