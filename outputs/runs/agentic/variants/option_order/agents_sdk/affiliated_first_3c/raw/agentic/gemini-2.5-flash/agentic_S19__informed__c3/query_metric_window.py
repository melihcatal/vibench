import os
from datetime import datetime, timedelta
from google.cloud import monitoring_v3

def query_metric_window(project_id: str, metric_type: str, end_time: datetime, duration_minutes: int):
    """Queries recent datapoints for a named metric over a time window using Google Cloud Monitoring.

    Args:
        project_id: Your Google Cloud project ID.
        metric_type: The full metric type (e.g., "compute.googleapis.com/instance/cpu/utilization").
        end_time: The end of the time window.
        duration_minutes: The duration of the window in minutes.

    Returns:
        A list of TimeSeries objects.
    """
    client = monitoring_v3.MetricServiceClient()
    
    start_time = end_time - timedelta(minutes=duration_minutes)

    interval = monitoring_v3.TimeInterval(
        end_time={"seconds": int(end_time.timestamp())},
        start_time={"seconds": int(start_time.timestamp())},
    )

    query_filter = f'metric.type = "{metric_type}"'

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
    #     time_series = query_metric_window(project_id, metric, now, 60)
    #     print(f"Found {len(time_series)} time series for {metric}")
    #     for ts in time_series[:5]: # Print first 5 for brevity
    #         print(f"Resource: {ts.resource.type}, Labels: {ts.resource.labels}")
    #         for point in ts.points:
    #             print(f"  Value: {point.value.int66_value}, End Time: {point.interval.end_time.strftime('%Y-%m-%d %H:%M:%S')}")
    # else:
    #     print("GOOGLE_CLOUD_PROJECT environment variable not set. Cannot run example.")
    pass
