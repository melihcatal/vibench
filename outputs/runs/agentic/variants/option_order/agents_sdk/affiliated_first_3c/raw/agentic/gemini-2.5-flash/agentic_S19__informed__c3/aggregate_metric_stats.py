import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3

def aggregate_metric_stats(project_id: str, metric_type: str, end_time: datetime, duration_minutes: int, aggregator_type: str = "MEAN", reducer_type: str = "MEAN"):
    """Retrieves aggregated statistics for a metric over a time window using Google Cloud Monitoring.

    Args:
        project_id: Your Google Cloud project ID.
        metric_type: The full metric type (e.g., "compute.googleapis.com/instance/cpu/utilization").
        end_time: The end of the time window.
        duration_minutes: The duration of the window in minutes.
        aggregator_type: How to aggregate points within a group (e.g., MEAN, MAX, MIN, SUM).
        reducer_type: How to combine aggregated time series (e.g., MEAN, MAX, MIN, SUM).

    Returns:
        A list of TimeSeries objects with aggregated data.
    """
    client = monitoring_v3.MetricServiceClient()

    start_time = end_time - timedelta(minutes=duration_minutes)

    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(end_time.timestamp())},
        start_time={"seconds": int(start_time.timestamp())},
    )

    query_filter = f'metric.type = "{metric_type}"'

    aggregation = monitoring_v3.Aggregation(
        alignment_period={"seconds": 60 * duration_minutes}, # Aggregate over the entire duration
        per_series_aligner=getattr(monitoring_v3.Aggregation.Aligner, aggregator_type, monitoring_v3.Aggregation.Aligner.ALIGN_MEAN),
        cross_series_reducer=getattr(monitoring_v3.Aggregation.Reducer, reducer_type, monitoring_v3.Aggregation.Reducer.REDUCE_MEAN),
        group_by_fields=["resource.type", "resource.labels.instance_name"] # Example grouping
    )

    result = client.list_time_series(
        request={
            "name": f"projects/{project_id}",
            "filter": query_filter,
            "interval": interval,
            "aggregation": aggregation,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )
    return list(result)

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS)
    # project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    # if project_id:
    #     metric = "logging.googleapis.com/log_entry_count"
    #     now = datetime.now()
    #     time_series = aggregate_metric_stats(project_id, metric, now, 60, aggregator_type="SUM", reducer_type="SUM")
    #     print(f"Found {len(time_series)} aggregated time series for {metric}")
    #     for ts in time_series[:5]:
    #         print(f"Resource: {ts.resource.type}, Labels: {ts.resource.labels}")
    #         for point in ts.points:
    #             print(f"  Value: {point.value.double_value if point.value.HasField('double_value') else point.value.int64_value}, End Time: {point.interval.end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    # else:
    #     print("GOOGLE_CLOUD_PROJECT environment variable not set. Cannot run example.")
    pass
