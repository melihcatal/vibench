import os
from typing import Any, Dict

from observability_client import ObservabilityClient
from observability_models import MetricWindowRequest, MetricResponse, normalize_points


def query_metric_window(metric_name: str, start_time: str, end_time: str, resource_filter: Dict[str, str] = None) -> MetricResponse:
    client = ObservabilityClient()
    request = MetricWindowRequest(metric_name=metric_name, start_time=start_time, end_time=end_time, resource_filter=resource_filter)
    payload = {
        "metricName": request.metric_name,
        "startTime": request.start_time,
        "endTime": request.end_time,
        "resourceFilter": request.resource_filter or {},
    }
    data = client.post("/metrics/query", payload)
    return MetricResponse(metric_name=metric_name, points=normalize_points(data.get("points", [])), statistics=data.get("statistics"), source="azure-monitor")
