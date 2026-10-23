import os
from google.cloud import monitoring_v3

# Set up client
client = monitoring_v3.MetricServiceClient()


# Function to query metric window
def query_metric_window(metric_name, start_time, end_time):
    # Define the project and resource
    project_name = "projects/{}".format(os.getenv("GOOGLE_CLOUD_PROJECT"))
    resource = monitoring_v3.types.monitored_resource.MonitoredResource(
        type="global", labels={}
    )

    # Define the interval
    interval = monitoring_v3.types.TimeInterval(
        start_time=start_time, end_time=end_time
    )

    # Define the metric
    metric = monitoring_v3.types.Metric(type=metric_name)

    # Create the request
    request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter='metric.type = "{}"'.format(metric_name),
        interval=interval,
        aggregation=None,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    # Query the metric
    time_series = client.list_time_series(request=request)
    return time_series
