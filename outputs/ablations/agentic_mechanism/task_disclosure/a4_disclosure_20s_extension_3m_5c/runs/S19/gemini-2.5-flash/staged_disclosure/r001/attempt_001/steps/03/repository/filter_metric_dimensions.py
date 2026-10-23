from google.cloud import monitoring_v3

def filter_metric_dimensions(project_id: str):
    """Queries metric data filtered by resource labels or dimensions."""
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    # Example: Query CPU utilization for a specific instance in Compute Engine
    # This example assumes you have a metric for CPU utilization
    # and that your Compute Engine instances have a "instance_name" label.
    query = """
        fetch gce_instance
        | metric 'agent.googleapis.com/cpu/utilization'
        | filter resource.labels.instance_name = 'my-instance'
        | group_by 1h, [value_utilization_mean: mean(value.utilization)]
        | every 1h
    """
    
    # Alternatively, you can filter by resource type and label directly in the query
    # without using MQL, by constructing a TimeSeries request.
    # For a more direct Pythonic way to filter without MQL:
    # filter_str = (
    #     'metric.type = "agent.googleapis.com/cpu/utilization" AND '
    #     'resource.type = "gce_instance" AND '
    #     'resource.labels.instance_name = "my-instance"'
    # )
    # interval = monitoring_v3.TimeInterval(
    #     end_time={"seconds": int(time.time())},
    #     start_time={"seconds": int(time.time() - 3600)}, # 1 hour ago
    # )
    # results = client.list_time_series(
    #     name=project_name,
    #     filter=filter_str,
    #     interval=interval,
    #     view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    # )
    # for result in results:
    #     print(result)

    request = monitoring_v3.QueryTimeSeriesRequest(
        name=project_name,
        query=query,
    )

    response = client.query_time_series(request=request)

    for time_series in response.time_series_data:
        print(f"Metric: {time_series.metric.type}")
        print(f"Resource Labels: {time_series.resource.labels}")
        for point in time_series.point_data:
            print(f"  Point: {point.values[0].double_value} at {point.time_interval.end_time.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    # or authenticate otherwise.
    # For example: export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key.json"
    PROJECT_ID = "your-gcp-project-id" 
    filter_metric_dimensions(PROJECT_ID)