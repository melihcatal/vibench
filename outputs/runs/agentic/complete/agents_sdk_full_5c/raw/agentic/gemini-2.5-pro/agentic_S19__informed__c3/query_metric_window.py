from datetime import datetime, timedelta, timezone
from google.cloud.monitoring_v3.services.metric_service import MetricServiceClient
from google.cloud.monitoring_v3.types import ListTimeSeriesRequest, TimeInterval
from google.protobuf.timestamp_pb2 import Timestamp

from observability_client import get_monitoring_client, get_project_id
from observability_models import TimeSeriesPoint, MetricTimeSeries

def query_metric_window(metric_type: str, minutes_ago: int = 60) -> list[MetricTimeSeries]:
    """
    Queries recent datapoints for a named metric over a time window.
    
    :param metric_type: The full name of the metric, e.g., "compute.googleapis.com/instance/cpu/utilization".
    :param minutes_ago: The duration of the time window in minutes from now.
    :return: A list of time series data.
    """
    client = get_monitoring_client()
    project_name = f"projects/{get_project_id()}"

    now = datetime.now(timezone.utc)
    start_time = now - timedelta(minutes=minutes_ago)
    
    interval = TimeInterval(
        start_time=Timestamp(seconds=int(start_time.timestamp())),
        end_time=Timestamp(seconds=int(now.timestamp()))
    )

    request = ListTimeSeriesRequest(
        name=project_name,
        filter=f'metric.type = "{metric_type}"',
        interval=interval,
        view=ListTimeSeriesRequest.TimeSeriesView.FULL,
    )
    
    results = client.list_time_series(request=request)
    
    output = []
    for result in results:
        points = [
            TimeSeriesPoint(timestamp=p.interval.end_time.isoformat(), value=p.value.double_value)
            for p in result.points
        ]
        series = MetricTimeSeries(
            metric_kind=str(result.metric_kind),
            value_type=str(result.value_type),
            points=points,
            resource_labels=dict(result.resource.labels),
            metric_labels=dict(result.metric.labels),
        )
        output.append(series)

    return output
