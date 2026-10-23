import datetime
import os
from typing import List, Dict, Any, Optional

from google.cloud import monitoring_v3

from observability_client import ObservabilityClient
from observability_models import MetricDataPoint, MetricQueryResult

def filter_metric_dimensions(
    project_id: str,
    metric_type: str,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    resource_labels: Optional[Dict[str, str]] = None,
    metric_labels: Optional[Dict[str, str]] = None,
) -> List[MetricQueryResult]:
    client = ObservabilityClient(project_id)
    monitoring_client = client.get_monitoring_client()
    project_name = client.get_project_name()

    interval = monitoring_v3.TimeInterval(
        end_time=end_time.isoformat(timespec="seconds") + "Z",
        start_time=start_time.isoformat(timespec="seconds") + "Z",
    )

    filter_parts = [f'metric.type = "{metric_type}"']

    if resource_labels:
        for key, value in resource_labels.items():
            filter_parts.append(f'resource.labels.{key} = "{value}"')

    if metric_labels:
        for key, value in metric_labels.items():
            filter_parts.append(f'metric.labels.{key} = "{value}"')

    filter_string = " AND ".join(filter_parts)

    query_results = []

    request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=filter_string,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    page_iterator = monitoring_client.list_time_series(request=request)

    for series in page_iterator:
        metric_name = series.metric.type
        resource_labels = dict(series.resource.labels)
        points = []
        for point in series.points:
            timestamp = point.interval.end_time.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)
            value = point.value.double_value if point.value.WhichOneof("value_type") == "double_value" else point.value.int64_value
            points.append(MetricDataPoint(timestamp=timestamp, value=value, labels=dict(series.metric.labels)))
        query_results.append(MetricQueryResult(metric_name=metric_name, resource_labels=resource_labels, points=points))

    return query_results
