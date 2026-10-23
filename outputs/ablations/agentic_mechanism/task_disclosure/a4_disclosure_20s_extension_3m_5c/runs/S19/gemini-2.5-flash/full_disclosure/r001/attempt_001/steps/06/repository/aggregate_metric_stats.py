from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2

def get_aggregated_metric_stats(
    project_id: str,
    metric_type: str,
    end_time_seconds: int,
    start_time_seconds: int,
    aggregator: str = "ALIGN_MEAN",  # e.g., ALIGN_MEAN, ALIGN_SUM, ALIGN_MAX, etc.
) -> dict:
    """
    Retrieves aggregated statistics for a metric over a time window using Google Cloud Monitoring.

    Args:
        project_id: Your Google Cloud Project ID.
        metric_type: The type of the metric (e.g., "compute.googleapis.com/instance/cpu/utilization").
        end_time_seconds: The end time of the time window in Unix epoch seconds.
        start_time_seconds: The start time of the time window in Unix epoch seconds.
        aggregator: The aggregation function to apply (e.g., "ALIGN_MEAN").

    Returns:
        A dictionary containing the aggregated time series data.
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    # Prepare time interval
    interval = monitoring_v3.TimeInterval()
    interval.end_time.seconds = end_time_seconds
    interval.start_time.seconds = start_time_seconds

    # Prepare aggregation
    aggregation = monitoring_v3.Aggregation()
    aggregation.alignment_period.seconds = 60  # Align to 1-minute intervals
    aggregation.per_series_aligner = getattr(monitoring_v3.Aggregation.Aligner, aggregator)
    aggregation.cross_series_reducer = monitoring_v3.Aggregation.Reducer.REDUCE_MEAN
    aggregation.group_by_fields.append("metric.labels.instance_name") # Example field to group by

    # Prepare filter
    # For custom metrics, use "metric.type = "custom.googleapis.com/my_metric_name""
    # For built-in metrics, use "metric.type = "{metric_type}""
    filter_str = f'metric.type = "{metric_type}"'

    request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=filter_str,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=aggregation,
    )

    response = client.list_time_series(request=request)

    results = []
    for ts in response.time_series:
        for point in ts.points:
            results.append({
                "value": point.value.double_value,
                "timestamp": point.interval.end_time.seconds,
                "metric_labels": {k: v for k, v in ts.metric.labels.items()},
                "resource_labels": {k: v for k, v in ts.resource.labels.items()},
            })

    return {"time_series_data": results}

