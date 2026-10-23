from google.cloud import monitoring_v3
from datetime import datetime

def compare_metric_series(project_id: str, metric_type: str, window_start: datetime, window_end: datetime, filter1: str, filter2: str):
    """
    Compares metric values for two resources or dimension filters over the same window.

    Args:
        project_id (str): Your Google Cloud project ID.
        metric_type (str): The metric type to query (e.g., 'agent.googleapis.com/memory/bytes_used').
        window_start (datetime): The start time of the comparison window.
        window_end (datetime): The end time of the comparison window.
        filter1 (str): Monitoring filter for the first series (e.g., 'resource.type = "gce_instance" AND resource.labels.instance_id = "12345"').
        filter2 (str): Monitoring filter for the second series.

    Returns:
        dict: A dictionary containing the time series data for both filters.
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    interval = monitoring_v3.TimeInterval(
        start_time={"seconds": int(window_start.timestamp())},
        end_time={"seconds": int(window_end.timestamp())},
    )

    # Query for the first series
    series1 = client.list_time_series(
        name=project_name,
        filter=f'metric.type = "{metric_type}" AND {filter1}',
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    # Query for the second series
    series2 = client.list_time_series(
        name=project_name,
        filter=f'metric.type = "{metric_type}" AND {filter2}',
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    return {
        "series1": [monitoring_v3.types.TimeSeries.to_dict(s) for s in series1],
        "series2": [monitoring_v3.types.TimeSeries.to_dict(s) for s in series2],
    }