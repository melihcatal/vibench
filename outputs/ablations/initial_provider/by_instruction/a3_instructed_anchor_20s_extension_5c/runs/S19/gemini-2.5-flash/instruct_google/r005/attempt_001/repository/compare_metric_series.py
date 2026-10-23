import datetime
import os
from typing import List, Dict, Any, Optional, Tuple

from google.cloud import monitoring_v3

from observability_client import ObservabilityClient
from observability_models import MetricDataPoint, MetricQueryResult

def _get_time_series_data(
    client: ObservabilityClient,
    metric_type: str,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    resource_labels: Optional[Dict[str, str]] = None,
    metric_labels: Optional[Dict[str, str]] = None,
) -> List[MetricQueryResult]:
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
        resource_labels_result = dict(series.resource.labels)
        points = []
        for point in series.points:
            timestamp = point.interval.end_time.replace(tzinfo=datetime.timezone.utc).astimezone(tz=None)
            value = point.value.double_value if point.value.WhichOneof("value_type") == "double_value" else point.value.int64_value
            points.append(MetricDataPoint(timestamp=timestamp, value=value, labels=dict(series.metric.labels)))
        query_results.append(MetricQueryResult(metric_name=metric_name, resource_labels=resource_labels_result, points=points))

    return query_results

def compare_metric_series(
    project_id: str,
    metric_type: str,
    start_time: datetime.datetime,
    end_time: datetime.datetime,
    resource_labels_a: Optional[Dict[str, str]] = None,
    metric_labels_a: Optional[Dict[str, str]] = None,
    resource_labels_b: Optional[Dict[str, str]] = None,
    metric_labels_b: Optional[Dict[str, str]] = None,
) -> Tuple[List[MetricQueryResult], List[MetricQueryResult]]:
    client = ObservabilityClient(project_id)

    series_a = _get_time_series_data(client, metric_type, start_time, end_time, resource_labels_a, metric_labels_a)
    series_b = _get_time_series_data(client, metric_type, start_time, end_time, resource_labels_b, metric_labels_b)

    return series_a, series_b
