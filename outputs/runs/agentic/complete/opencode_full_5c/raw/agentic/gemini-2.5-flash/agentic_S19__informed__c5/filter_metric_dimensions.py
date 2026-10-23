from datetime import datetime, timedelta
from typing import Dict
from observability_client import ObservabilityClient
from observability_models import normalize_time_series, build_metric_filter
from google.cloud import monitoring_v3


def filter_metric_dimensions(
    metric_name: str, end_time: datetime, minutes: int, resource_labels: Dict[str, str]
) -> list:
    client = ObservabilityClient()
    monitoring_client = client.get_monitoring_client()
    project_name = client.get_project_name()

    start_time = end_time - timedelta(minutes=minutes)

    interval = monitoring_v3.TimeInterval(
        end_time=end_time.isoformat() + "Z",
        start_time=start_time.isoformat() + "Z",
    )

    query_filter = build_metric_filter(metric_name, resource_labels)

    response = monitoring_client.list_time_series(
        name=project_name,
        filter=query_filter,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    return normalize_time_series([series.to_dict() for series in response])
