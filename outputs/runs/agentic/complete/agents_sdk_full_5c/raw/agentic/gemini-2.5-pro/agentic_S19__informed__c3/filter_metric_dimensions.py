from datetime import datetime, timedelta, timezone
from typing import Dict
from google.cloud.monitoring_v3.types import ListTimeSeriesRequest, TimeInterval
from google.protobuf.timestamp_pb2 import Timestamp

from observability_client import get_monitoring_client, get_project_id
from observability_models import MetricTimeSeries, TimeSeriesPoint

def query_metric_with_dimensions(
    metric_type: str, 
    dimensions: Dict[str, str],
    minutes_ago: int = 60
) -> list[MetricTimeSeries]:
    """
    Queries metric data filtered by resource labels or dimensions.
    
    :param metric_type: The metric to query.
    :param dimensions: A dictionary of resource or metric labels to filter by.
    :param minutes_ago: The time window in minutes.
    :return: A list of filtered time series data.
    """
    client = get_monitoring_client()
    project_name = f"projects/{get_project_id()}"

    now = datetime.now(timezone.utc)
    start_time = now - timedelta(minutes=minutes_ago)
    
    interval = TimeInterval(
        start_time=Timestamp(seconds=int(start_time.timestamp())),
        end_time=Timestamp(seconds=int(now.timestamp()))
    )
    
    dimension_filters = " AND ".join(
        [f'resource.labels.{key} = "{value}"' for key, value in dimensions.items()]
    )
    filter_string = f'metric.type = "{metric_type}" AND {dimension_filters}'

    request = ListTimeSeriesRequest(
        name=project_name,
        filter=filter_string,
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
