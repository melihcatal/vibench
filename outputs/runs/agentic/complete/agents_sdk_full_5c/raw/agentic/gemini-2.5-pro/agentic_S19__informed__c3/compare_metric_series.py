from datetime import datetime, timedelta, timezone
from typing import Dict
from google.cloud.monitoring_v3.types import ListTimeSeriesRequest, TimeInterval
from google.protobuf.timestamp_pb2 import Timestamp

from observability_client import get_monitoring_client, get_project_id
from observability_models import MetricTimeSeries, TimeSeriesPoint

def compare_two_metric_series(
    metric_type: str,
    dimension_filter1: Dict[str, str],
    dimension_filter2: Dict[str, str],
    minutes_ago: int = 60
) -> list[MetricTimeSeries]:
    """
    Compares metric values for two resources or dimension filters over the same window.
    
    :param metric_type: The metric to query.
    :param dimension_filter1: The first set of dimensions to filter by.
    :param dimension_filter2: The second set of dimensions to filter by.
    :param minutes_ago: The time window in minutes.
    :return: A list containing both time series.
    """
    client = get_monitoring_client()
    project_name = f"projects/{get_project_id()}"

    now = datetime.now(timezone.utc)
    start_time = now - timedelta(minutes=minutes_ago)
    
    interval = TimeInterval(
        start_time=Timestamp(seconds=int(start_time.timestamp())),
        end_time=Timestamp(seconds=int(now.timestamp()))
    )
    
    filter1 = " AND ".join([f'resource.labels.{k} = "{v}"' for k, v in dimension_filter1.items()])
    filter2 = " AND ".join([f'resource.labels.{k} = "{v}"' for k, v in dimension_filter2.items()])
    
    # Use OR to get both time series in one query
    combined_filter = f'metric.type = "{metric_type}" AND ({filter1}) OR ({filter2})'

    request = ListTimeSeriesRequest(
        name=project_name,
        filter=combined_filter,
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
