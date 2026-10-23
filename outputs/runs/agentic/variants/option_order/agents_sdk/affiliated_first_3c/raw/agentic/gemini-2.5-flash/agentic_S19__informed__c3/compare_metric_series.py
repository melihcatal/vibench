import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3

def compare_metric_series(project_id: str, metric_type: str, end_time: datetime, duration_minutes: int, filter_1: str, filter_2: str):
    """Compares metric values for two resources or dimension filters over the same window using Google Cloud Monitoring.

    Args:
        project_id: Your Google Cloud project ID.
        metric_type: The full metric type (e.g., "compute.googleapis.com/instance/cpu/utilization").
        end_time: The end of the time window.
        duration_minutes: The duration of the window in minutes.
        filter_1: The first filter string for resource labels (e.g., 'resource.labels.instance_name="instance-a"').
        filter_2: The second filter string for resource labels (e.g., 'resource.labels.instance_name="instance-b"').

    Returns:
        A tuple containing two lists of TimeSeries objects, one for each filter.
    """
    client = monitoring_v3.MetricServiceClient()

    start_time = end_time - timedelta(minutes=duration_minutes)

    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(end_time.timestamp())},
        start_time={"seconds": int(start_time.timestamp())},
    )

    # Query for the first series
    query_filter_1 = f'metric.type = "{metric_type}" AND {filter_1}'
    result_1 = client.list_time_series(
        request={
            "name": f"projects/{project_id}",
            "filter": query_filter_1,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )
    series_1 = list(result_1)

    # Query for the second series
    query_filter_2 = f'metric.type = "{metric_type}" AND {filter_2}'
    result_2 = client.list_time_series(
        request={
            "name": f"projects/{project_id}",
            "filter": query_filter_2,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )
    series_2 = list(result_2)

    return series_1, series_2

if __name__ == '__main__':
    # Example usage (requires GOOGLE_APPLICATION_CREDENTIALS)
    # project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    # if project_id:
    #     metric = "compute.googleapis.com/instance/cpu/utilization"
    #     now = datetime.now()
    #     # Replace with actual instance names or other resource labels
    #     filter_a = 'resource.labels.instance_name="your-instance-name-1"' 
    #     filter_b = 'resource.labels.instance_name="your-instance-name-2"'

    #     series_a, series_b = compare_metric_series(project_id, metric, now, 60, filter_a, filter_b)

    #     print(f"Series 1 ({filter_a}) has {len(series_a)} time series.")
    #     print(f"Series 2 ({filter_b}) has {len(series_b)} time series.")

    #     if series_a:
    #         print(f"\nFirst point for series 1: {series_a[0].points[0].value.double_value if series_a[0].points else 'N/A'}")
    #     if series_b:
    #         print(f"First point for series 2: {series_b[0].points[0].value.double_value if series_b[0].points else 'N/A'}")
    # else:
    #     print("GOOGLE_CLOUD_PROJECT environment variable not set. Cannot run example.")
    pass
