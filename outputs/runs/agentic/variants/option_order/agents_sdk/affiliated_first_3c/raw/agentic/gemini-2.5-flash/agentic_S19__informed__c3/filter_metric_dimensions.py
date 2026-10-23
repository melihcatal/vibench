import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3

def filter_metric_dimensions(project_id: str, metric_type: str, end_time: datetime, duration_minutes: int, resource_filter: str):
    """Queries metric data filtered by resource labels or dimensions using Google Cloud Monitoring.

    Args:
        project_id: Your Google Cloud project ID.
        metric_type: The full metric type (e.g., "compute.googleapis.com/instance/cpu/utilization").
        end_time: The end of the time window.
        duration_minutes: The duration of the window in minutes.
        resource_filter: A filter string for resource labels (e.g., 'resource.labels.instance_name="my-instance"').

    Returns:
        A list of TimeSeries objects.
    """
    client = monitoring_v3.MetricServiceClient()

    start_time = end_time - timedelta(minutes=duration_minutes)

    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(end_time.timestamp())},
        start_time={"seconds": int(start_time.timestamp())},
    )

    # Combine metric type filter with resource filter
    query_filter = f'metric.type = "{metric_type}" AND {resource_filter}'

    result = client.list_time_series(
        request={
            "name": f"projects/{project_id}",
            "filter": query_filter,
            "interval": interval,
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
    #     # Example: Filter by a specific resource instance. Replace with a real value if testing.
    #     resource_filter_str = 'resource.labels.log_id="cloudaudit.googleapis.com%2Factivity"' # A common log ID
    #     time_series = filter_metric_dimensions(project_id, metric, now, 60, resource_filter_str)
    #     print(f"Found {len(time_series)} time series for {metric} with filter '{resource_filter_str}'")
    #     for ts in time_series[:5]:
    #         print(f"Resource: {ts.resource.type}, Labels: {ts.resource.labels}")
    #         for point in ts.points:
    #             print(f"  Value: {point.value.int64_value}, End Time: {point.interval.end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    # else:
    #     print("GOOGLE_CLOUD_PROJECT environment variable not set. Cannot run example.")
    pass
