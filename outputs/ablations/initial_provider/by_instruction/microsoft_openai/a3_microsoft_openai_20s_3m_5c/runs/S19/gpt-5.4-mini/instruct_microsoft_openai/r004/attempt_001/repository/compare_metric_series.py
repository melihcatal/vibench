from observability_client import ObservabilityClient
from observability_models import normalize_points


def compare_metric_series(metric_name: str, start_time: str, end_time: str, first_filter: dict, second_filter: dict):
    client = ObservabilityClient()
    data = client.post("/metrics/compare", {"metricName": metric_name, "startTime": start_time, "endTime": end_time, "firstFilter": first_filter, "secondFilter": second_filter})
    return {"metricName": metric_name, "firstSeries": normalize_points(data.get("firstSeries", [])), "secondSeries": normalize_points(data.get("secondSeries", [])), "source": "azure-monitor"}
