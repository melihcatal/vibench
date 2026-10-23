import datetime
from google.cloud import monitoring_v3  # Provider-identifying signal
from observability_client import get_monitoring_client
from observability_models import MetricQuery, MetricResult


def query_metric_window(
    project_id: str,
    metric_type: str,
    end_time: datetime.datetime,
    start_time: datetime.datetime,
) -> MetricResult:
    client = get_monitoring_client()
    project_name = f"projects/{project_id}"

    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(end_time.timestamp())},
        start_time={"seconds": int(start_time.timestamp())},
    )

    # Google Cloud Monitoring uses a filter string to specify the metric type
    filter_str = f'metric.type = "{metric_type}"'

    response = client.list_time_series(
        name=project_name,
        filter=filter_str,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    return MetricResult.from_response(response)
