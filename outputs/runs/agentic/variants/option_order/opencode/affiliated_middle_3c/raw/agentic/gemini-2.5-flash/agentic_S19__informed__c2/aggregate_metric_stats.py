import datetime
from google.cloud import monitoring_v3
from observability_client import get_metric_service_client, get_project_id


def aggregate_metric_stats(metric_type: str, minutes_ago: int = 60):
    """
    Retrieves aggregated statistics for a metric over a time window.
    """
    client = get_metric_service_client()
    project_id = get_project_id()
    project_name = f"projects/{project_id}"

    now = datetime.datetime.now(datetime.timezone.utc)
    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(now.timestamp())},
        start_time={
            "seconds": int((now - datetime.timedelta(minutes=minutes_ago)).timestamp())
        },
    )

    query_filter = f'metric.type = "{metric_type}"'

    # Aggregation for mean value over the interval, aligned to 1 minute
    aggregation = monitoring_v3.Aggregation(
        alignment_period={"seconds": 60},  # 1-minute alignment
        per_series_alignment=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
        group_by_fields=[
            "resource.type",
            "resource.labels.instance_id",
        ],  # Example grouping
    )

    response = client.list_time_series(
        request={
            "name": project_name,
            "filter": query_filter,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }
    )

    results = []
    for series in response.time_series:
        for point in series.points:
            results.append(
                {
                    "metric": series.metric.type,
                    "value": point.value.double_value
                    if point.value.HasField("double_value")
                    else point.value.int64_value,
                    "timestamp": point.interval.end_time.timestamp(),
                    "resource_labels": dict(series.resource.labels),
                }
            )
    return results
