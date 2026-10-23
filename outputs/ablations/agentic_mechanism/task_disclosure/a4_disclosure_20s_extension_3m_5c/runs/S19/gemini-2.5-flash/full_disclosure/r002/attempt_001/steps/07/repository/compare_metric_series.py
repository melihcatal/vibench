
from google.cloud import monitoring_v3

def compare_metric_series(
    project_id: str,
    metric_type: str,
    filter_a: str,
    filter_b: str,
    interval_seconds: int,
    window_minutes: int,
):
    """Compares metric values for two resources or dimension filters over the same window.

    Args:
        project_id: Your Google Cloud project ID.
        metric_type: The type of metric to query (e.g., "compute.googleapis.com/instance/cpu/utilization").
        filter_a: The monitoring filter for the first series (e.g., 'resource.type = "gce_instance" AND resource.labels.instance_id = "12345"').
        filter_b: The monitoring filter for the second series.
        interval_seconds: The sampling interval in seconds.
        window_minutes: The duration of the comparison window in minutes.
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = client.common.time_interval.now()
    end_time = now
    start_time = now - client.common.time_interval.timedelta(minutes=window_minutes)

    interval = monitoring_v3.TimeInterval(end_time=end_time, start_time=start_time)

    aggregation = monitoring_v3.Aggregation(
        alignment_period=client.common.time_interval.timedelta(seconds=interval_seconds),
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
    )

    # Query for the first series
    series_a = client.list_time_series(
        name=project_name,
        filter=f'metric.type = "{metric_type}" AND {filter_a}',
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=aggregation,
    )

    # Query for the second series
    series_b = client.list_time_series(
        name=project_name,
        filter=f'metric.type = "{metric_type}" AND {filter_b}',
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        aggregation=aggregation,
    )

    print(f"Metric Series A for {metric_type} with filter: {filter_a}")
    for ts in series_a:
        print(ts)

    print(f"Metric Series B for {metric_type} with filter: {filter_b}")
    for ts in series_b:
        print(ts)

    # Further comparison logic would go here, e.g.,
    # - Extracting values from time series
    # - Performing statistical comparison
    # - Generating a report or visualization
