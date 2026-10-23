
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2

def query_metric_window(project_id: str, metric_type: str, end_time_seconds: int, window_minutes: int):
    """
    Queries recent datapoints for a named metric over a time window using Google Cloud Monitoring.

    Args:
        project_id: Your Google Cloud project ID.
        metric_type: The type of metric to query (e.g., "compute.googleapis.com/instance/cpu/utilization").
        end_time_seconds: The end of the time window in Unix timestamp seconds.
        window_minutes: The duration of the time window in minutes.
    """
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    # Prepare time interval
    end_time = timestamp_pb2.Timestamp()
    end_time.seconds = end_time_seconds
    start_time = timestamp_pb2.Timestamp()
    start_time.seconds = end_time_seconds - (window_minutes * 60)

    interval = monitoring_v3.TimeInterval(end_time=end_time, start_time=start_time)

    # Prepare filter
    # For simplicity, this example assumes no resource labels or metric labels for filtering beyond metric_type.
    # A more complex scenario might require specific resource.type and metric.labels in the filter.
    filter_string = f'metric.type = "{metric_type}"'

    # Create request
    request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=filter_string,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    # Execute the query
    response = client.list_time_series(request=request)

    # Process and print results
    print(f"Metric: {metric_type}")
    for series in response.time_series:
        print(f"  Resource: {series.resource.type}, Labels: {series.resource.labels}")
        for point in series.points:
            print(f"    Value: {point.value.double_value if point.value.HasField('double_value') else point.value.int64_value}, Time: {point.interval.end_time.seconds}")

if __name__ == "__main__":
    # Example Usage: Replace with your actual project ID and metric type
    # To get a list of available metrics, you can use the 'gcloud monitoring metrics list' command
    # or refer to Google Cloud documentation.
    # Example metric for CPU utilization: "compute.googleapis.com/instance/cpu/utilization"
    # Make sure you have authenticated your gcloud environment (e.g., 'gcloud auth application-default login')
    
    # You will need to replace 'YOUR_PROJECT_ID' with your actual Google Cloud Project ID.
    # You will also need to choose an appropriate metric_type that exists in your project.
    # For testing, you can use a common metric like 'agent.googleapis.com/agent/health/uptime'
    # or 'logging.googleapis.com/log_entry_count' if you have logs.

    # This example queries for the last 5 minutes of data.
    import time
    current_time_seconds = int(time.time())
    query_metric_window(
        project_id="YOUR_PROJECT_ID",  # Replace with your project ID
        metric_type="compute.googleapis.com/instance/cpu/utilization", # Replace with your metric type
        end_time_seconds=current_time_seconds,
        window_minutes=5
    )
