from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2

def get_aggregated_metric_stats(project_id: str, metric_type: str, start_time: float, end_time: float):
    """
    Retrieves aggregated statistics for a metric over a time window using Google Cloud Monitoring.

    Args:
        project_id (str): Your Google Cloud project ID.
        metric_type (str): The type of the metric (e.g., "compute.googleapis.com/instance/cpu/utilization").
        start_time (float): The start of the time window in Unix timestamp seconds.
        end_time (float): The end of the time window in Unix timestamp seconds.

    Returns:
        list: A list of aggregated time series data.
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = client.project_path(project_id)

    now = timestamp_pb2.Timestamp()
    now.seconds = int(end_time)
    now.nanos = int((end_time - int(end_time)) * 10**9)

    interval = monitoring_v3.TimeInterval()
    interval.end_time = now
    interval.start_time.seconds = int(start_time)
    interval.start_time.nanos = int((start_time - int(start_time)) * 10**9)

    aggregation = monitoring_v3.Aggregation()
    aggregation.alignment_period.seconds = 60 * 5  # 5-minute aggregation
    aggregation.per_series_aligner = monitoring_v3.Aggregation.Aligner.ALIGN_MEAN
    aggregation.cross_series_reducer = monitoring_v3.Aggregation.Reducer.REDUCE_MEAN
    aggregation.group_by_fields.append("metric.labels.instance_name") # Example group by field

    results = client.list_time_series(
        name=project_name,
        filter=f'metric.type = "{metric_type}"',
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=aggregation,
    )

    return list(results)
