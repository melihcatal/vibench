from datetime import datetime, timedelta
from observability_client import ObservabilityClient
from observability_models import normalize_time_series
from google.cloud import monitoring_v3


def query_metric_window(metric_name: str, end_time: datetime, minutes: int) -> list:
    client = ObservabilityClient()
    monitoring_client = client.get_monitoring_client()
    project_name = client.get_project_name()

    start_time = end_time - timedelta(minutes=minutes)

    interval = monitoring_v3.TimeInterval(
        end_time=end_time.isoformat() + "Z",
        start_time=start_time.isoformat() + "Z",
    )

    query_filter = f'metric.type = "{metric_name}"'

    # Using MetricServiceClient directly to query time series
    # This is a basic query, more complex queries might use aggregation or alignment
    response = monitoring_client.list_time_series(
        name=project_name,
        filter=query_filter,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    return normalize_time_series([series.to_dict() for series in response])
