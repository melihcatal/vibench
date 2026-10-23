from datetime import datetime, timedelta
from typing import Dict
from observability_client import ObservabilityClient
from observability_models import normalize_time_series, build_metric_filter
from google.cloud import monitoring_v3


def compare_metric_series(
    metric_name: str,
    end_time: datetime,
    minutes: int,
    resource_labels_1: Dict[str, str],
    resource_labels_2: Dict[str, str],
) -> Dict[str, list]:
    client = ObservabilityClient()
    monitoring_client = client.get_monitoring_client()
    project_name = client.get_project_name()

    start_time = end_time - timedelta(minutes=minutes)

    interval = monitoring_v3.TimeInterval(
        end_time=end_time.isoformat() + "Z",
        start_time=start_time.isoformat() + "Z",
    )

    # Query for the first series
    filter_1 = build_metric_filter(metric_name, resource_labels_1)
    response_1 = monitoring_client.list_time_series(
        name=project_name,
        filter=filter_1,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )
    series_1 = normalize_time_series([series.to_dict() for series in response_1])

    # Query for the second series
    filter_2 = build_metric_filter(metric_name, resource_labels_2)
    response_2 = monitoring_client.list_time_series(
        name=project_name,
        filter=filter_2,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )
    series_2 = normalize_time_series([series.to_dict() for series in response_2])

    return {
        "series_1": series_1,
        "series_2": series_2,
    }
