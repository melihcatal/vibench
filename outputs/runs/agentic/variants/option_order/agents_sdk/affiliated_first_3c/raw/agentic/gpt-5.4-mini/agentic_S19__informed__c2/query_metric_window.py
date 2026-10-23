from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from observability_client import DatadogMetricsClient
from observability_models import MetricWindowRequest, parse_series_payload, to_query

DATADOG_METRIC_QUERY_PREFIX = "avg:"


def query_metric_window(metric_name: str, start: datetime, end: datetime) -> Dict[str, Any]:
    client = DatadogMetricsClient()
    request = MetricWindowRequest(metric_name=metric_name, start=start, end=end)
    payload = client.query(f"{DATADOG_METRIC_QUERY_PREFIX}{request.metric_name}{{*}}", request.start, request.end)
    return {"request": request, "response": parse_series_payload(payload)}
