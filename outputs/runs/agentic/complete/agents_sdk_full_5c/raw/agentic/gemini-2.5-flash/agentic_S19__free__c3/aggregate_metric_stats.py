from observability_client import get_monitoring_client
from google.cloud import monitoring_v3

def aggregate_metric_stats(project_id: str, metric_type: str, end_time_seconds: int, duration_seconds: int,
                           agg_reducer: monitoring_v3.Aggregation.Reducer, agg_period_seconds: int):
    client = get_monitoring_client()
    project_name = f"projects/{project_id}"

    interval = monitoring_v3.types.TimeInterval()
    interval.end_time.seconds = end_time_seconds
    interval.end_time.nanos = 0
    interval.start_time.seconds = interval.end_time.seconds - duration_seconds
    interval.start_time.nanos = 0

    aggregation = monitoring_v3.types.Aggregation()
    aggregation.alignment_period.seconds = agg_period_seconds
    aggregation.per_series_reducer = agg_reducer
    aggregation.group_by_fields.append("resource.instance_id") # Example grouping

    response = client.list_time_series(
        name=project_name,
        filter=f'metric.type = "{metric_type}"',
        interval=interval,
        view=monitoring_v3.types.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=aggregation
    )

    aggregated_data = []
    for ts in response:
        for point in ts.points:
            aggregated_data.append({
                "resource": ts.resource.labels,
                "metric_labels": ts.metric.labels,
                "value": point.value.double_value or point.value.int64_value,
                "end_time": point.interval.end_time.rfc3339()
            })
    return aggregated_data
