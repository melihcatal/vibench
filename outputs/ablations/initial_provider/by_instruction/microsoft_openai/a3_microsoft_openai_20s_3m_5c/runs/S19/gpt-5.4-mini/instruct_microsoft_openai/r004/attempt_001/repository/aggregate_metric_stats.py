from observability_client import ObservabilityClient
from observability_models import MetricResponse, normalize_points


def aggregate_metric_stats(metric_name: str, start_time: str, end_time: str):
    client = ObservabilityClient()
    data = client.post("/metrics/aggregate", {"metricName": metric_name, "startTime": start_time, "endTime": end_time})
    return MetricResponse(metric_name=metric_name, points=normalize_points(data.get("points", [])), statistics=data.get("statistics"), source="azure-monitor")
