import datetime
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client, get_project_id
from observability_models import MetricQuery, TimeSeriesData
from typing import List, Dict, Any

def aggregate_metric_stats(query: MetricQuery, aligner: monitoring_v3.Aggregation.Aligner = monitoring_v3.Aggregation.Aligner.ALIGN_MEAN, reducer: monitoring_v3.Aggregation.Reducer = monitoring_v3.Aggregation.Reducer.REDUCE_MEAN) -> List[TimeSeriesData]:
    """
    Retrieves aggregated statistics for a metric over a time window using Google Cloud Monitoring.
    """
    client = get_monitoring_client()
    project_id = query.project_id or get_project_id()
    project_name = f"projects/{project_id}"

    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(query.end_time.timestamp())},
        start_time={"seconds": int(query.start_time.timestamp())},
    )

    metric_filter = f'metric.type = "{query.metric_type}"'
    if query.filters:
        metric_filter += f' AND {query.filters}'

    aggregation = monitoring_v3.Aggregation(
        alignment_period={"seconds": query.interval_seconds},
        per_series_aligner=aligner,
        cross_series_reducer=reducer,
        group_by_fields=["resource.type", "resource.labels.instance_id"] # Example grouping, adjust as needed
    )

    results = client.list_time_series(
        name=project_name,
        filter=metric_filter,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=aggregation,
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
