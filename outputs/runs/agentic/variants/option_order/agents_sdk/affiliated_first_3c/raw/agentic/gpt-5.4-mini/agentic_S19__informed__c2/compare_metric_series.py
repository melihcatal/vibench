from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from observability_client import DatadogMetricsClient
from observability_models import MetricCompareRequest, parse_series_payload, to_query


def compare_metric_series(metric_name: str, start: datetime, end: datetime, left_filters: Dict[str, str], right_filters: Dict[str, str]) -> Dict[str, Any]:
    client = DatadogMetricsClient()
    request = MetricCompareRequest(metric_name=metric_name, start=start, end=end, left_filters=left_filters, right_filters=right_filters)
    left_query = f"avg:{request.metric_name}{to_query(request.left_filters)}"
    right_query = f"avg:{request.metric_name}{to_query(request.right_filters)}"
    left_response = parse_series_payload(client.query(left_query, request.start, request.end))
    right_response = parse_series_payload(client.query(right_query, request.start, request.end))
    return {"request": request, "left": left_response, "right": right_response}
