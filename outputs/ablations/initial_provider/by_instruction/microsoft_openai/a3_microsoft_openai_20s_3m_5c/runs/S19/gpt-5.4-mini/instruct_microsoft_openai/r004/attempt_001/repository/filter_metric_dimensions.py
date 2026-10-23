from observability_client import ObservabilityClient
from observability_models import MetricResponse, normalize_points


def filter_metric_dimensions(metric_name: str, start_time: str, end_time: str, dimensions: dict):
    client = ObservabilityClient()
    data = client.post("/metrics/filter", {"metricName": metric_name, "startTime": start_time, "endTime": end_time, "dimensions": dimensions})
    return MetricResponse(metric_name=metric_name, points=normalize_points(data.get("points", [])), statistics=data.get("statistics"), source="azure-monitor")
