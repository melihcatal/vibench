import datetime
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client, get_project_id
from observability_models import MetricQuery, TimeSeriesData
from typing import List

def filter_metric_dimensions(query: MetricQuery) -> List[TimeSeriesData]:
    """
    Queries metric data filtered by resource labels or dimensions using Google Cloud Monitoring.
    The 'filters' field in MetricQuery is crucial here.
    """
    client = get_monitoring_client()
    project_id = query.project_id or get_project_id()
    project_name = f"projects/{project_id}"

    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(query.end_time.timestamp())},
        start_time={"seconds": int(query.start_time.timestamp())},
    )

    # Construct the filter string with both metric type and dimension filters
    metric_filter = f'metric.type = "{query.metric_type}"'
    if query.filters:
        metric_filter += f' AND {query.filters}' # query.filters should contain resource.labels.key="value" etc.

    results = client.list_time_series(
        name=project_name,
        filter=metric_filter,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    all_time_series_data = []
    for time_series in results:
        points = []
        for point in time_series.points:
            point_value = None
            if point.value.double_value is not None:
                point_value = point.value.double_value
            elif point.value.int64_value is not None:
                point_value = point.value.int64_value
            elif point.value.string_value is not None:
                point_value = point.value.string_value
            elif point.value.bool_value is not None:
                point_value = point.value.bool_value

            points.append({
                "timestamp": point.interval.end_time.timestamp(),
                "value": point_value
            })
        all_time_series_data.append(TimeSeriesData(
            points=points,
            resource_labels=dict(time_series.resource.labels),
            metric_labels=dict(time_series.metric.labels)
        ))
    return all_time_series_data
