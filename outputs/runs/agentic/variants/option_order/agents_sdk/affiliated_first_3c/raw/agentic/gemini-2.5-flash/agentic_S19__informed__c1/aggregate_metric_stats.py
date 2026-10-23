from google.cloud import monitoring_v3
from datetime import datetime, timedelta

def aggregate_metric_stats(project_id: str, metric_type: str, end_time: datetime, minutes: int):
    """
    Retrieves aggregated statistics for a metric over a time window.
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    start_time = end_time - timedelta(minutes=minutes)

    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(end_time.timestamp())},
        start_time={"seconds": int(start_time.timestamp())},
    )

    # Example aggregation: MEAN over 1-minute alignment period
    aggregation = monitoring_v3.Aggregation(
        alignment_period={"seconds": 60},  # 1 minute
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        cross_series_reducer=monitoring_v3.Aggregation.Reducer.REDUCE_MEAN,
        group_by_fields=["resource.metric.type"], # Group by metric type
    )

    query = f'fetch gce_instance :: {metric_type}'

    results = client.query_time_series(
        name=project_name,
        query=query,
        interval=interval,
        aggregation=aggregation,
    )

    aggregated_stats = []
    for page in results.pages:
        for time_series in page.time_series:
            for point in time_series.points:
                aggregated_stats.append({
                    "timestamp": point.interval.end_time.strftime("%Y-%m-%dT%H:%M:%SZ"),
                    "value": point.value.double_value or point.value.int64_value,
                    "metric": time_series.metric.type
                })
    return aggregated_stats
