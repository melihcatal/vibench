import os
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2

def get_aggregated_metric_stats(
    project_id: str,
    metric_type: str,
    end_time_seconds: int,
    start_time_seconds: int,
    aggregator: str = "AGGREGATE_MEAN",
    alignment_period_seconds: int = 300, # 5 minutes
):
    """Retrieves aggregated statistics for a metric over a time window.

    Args:
        project_id: Your Google Cloud Project ID.
        metric_type: The type of the metric (e.g., "compute.googleapis.com/instance/cpu/usage_time").
        end_time_seconds: End time of the time window in Unix seconds.
        start_time_seconds: Start time of the time window in Unix seconds.
        aggregator: The aggregation function to apply (e.g., "AGGREGATE_MEAN", "AGGREGATE_MAX", "AGGREGATE_MIN").
        alignment_period_seconds: The alignment period in seconds for aggregation.
    
    Returns:
        A list of aggregated metric data points.
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    # Set the time interval
    interval = monitoring_v3.TimeInterval(
        end_time=timestamp_pb2.Timestamp(seconds=end_time_seconds),
        start_time=timestamp_pb2.Timestamp(seconds=start_time_seconds),
    )

    # Set the aggregation parameters
    aggregation = monitoring_v3.Aggregation(
        alignment_period=timestamp_pb2.Duration(seconds=alignment_period_seconds),
        per_series_aligner=getattr(monitoring_v3.Aggregation.Aligner, "ALIGN_" + aggregator.upper()),
        cross_series_reducer=getattr(monitoring_v3.Aggregation.Reducer, aggregator.upper()),
        group_by_fields=["resource.labels.instance_name"] if "instance" in metric_type else [],
    )

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": f'metric.type = "{metric_type}"',
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }
    )

    aggregated_data = []
    for series in results:
        for point in series.points:
            aggregated_data.append(
                {
                    "start_time": point.interval.start_time.seconds,
                    "end_time": point.interval.end_time.seconds,
                    "value": point.value.double_value or point.value.int64_value,
                    "resource": series.resource.labels,
                    "metric_labels": series.metric.labels
                }
            )
    return aggregated_data
