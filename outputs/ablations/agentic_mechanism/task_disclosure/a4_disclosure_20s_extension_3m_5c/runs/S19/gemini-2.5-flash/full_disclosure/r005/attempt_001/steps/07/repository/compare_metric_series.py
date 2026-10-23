from google.cloud import monitoring_v3

def compare_metric_series(
    project_id: str,
    metric_type: str,
    filter_a: str,
    filter_b: str,
    start_time: str,
    end_time: str,
):
    """Compares metric values for two resources or dimension filters over the same window
    using Google Cloud Monitoring.

    Args:
        project_id: Your Google Cloud project ID.
        metric_type: The type of the metric (e.g., "compute.googleapis.com/instance/cpu/usage").
        filter_a: The monitoring filter for the first series (e.g., 'resource.instance_id = "123"').
        filter_b: The monitoring filter for the second series (e.g., 'resource.instance_id = "456"').
        start_time: Start time for the query in RFC3339 format (e.g., "2023-01-01T00:00:00Z").
        end_time: End time for the query in RFC3339 format (e.g., "2023-01-01T01:00:00Z").

    Returns:
        A dictionary containing the time series data for both filters.
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = client.project_path(project_id)

    # Common query parameters
    interval = monitoring_v3.TimeInterval(
        start_time={"seconds": int(
            monitoring_v3.types.Timestamp.from_rfc3339(start_time).seconds)},
        end_time={"seconds": int(
            monitoring_v3.types.Timestamp.from_rfc3339(end_time).seconds)},
    )
    
    # Query for filter A
    series_a = client.list_time_series(
        name=project_name,
        filter=f'metric.type = "{metric_type}" AND {filter_a}',
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    # Query for filter B
    series_b = client.list_time_series(
        name=project_name,
        filter=f'metric.type = "{metric_type}" AND {filter_b}',
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    return {
        "series_a": [series.to_dict() for series in series_a],
        "series_b": [series.to_dict() for series in series_b],
    }
