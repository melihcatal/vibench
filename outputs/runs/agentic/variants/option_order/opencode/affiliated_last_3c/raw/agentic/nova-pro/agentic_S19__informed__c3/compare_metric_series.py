import os
from google.cloud import monitoring_v3

# Set up client
client = monitoring_v3.MetricServiceClient()


# Function to compare metric series
def compare_metric_series(metric_name, start_time, end_time, labels1, labels2):
    # Define the project and resource
    project_name = "projects/{}".format(os.getenv("GOOGLE_CLOUD_PROJECT"))
    resource1 = monitoring_v3.types.monitored_resource.MonitoredResource(
        type="global", labels=labels1
    )
    resource2 = monitoring_v3.types.monitored_resource.MonitoredResource(
        type="global", labels=labels2
    )

    # Define the interval
    interval = monitoring_v3.types.TimeInterval(
        start_time=start_time, end_time=end_time
    )

    # Define the metric
    metric = monitoring_v3.types.Metric(type=metric_name)

    # Create the requests
    request1 = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter='metric.type = "{}"'.format(metric_name),
        interval=interval,
        aggregation=None,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        resource=resource1,
    )
    request2 = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter='metric.type = "{}"'.format(metric_name),
        interval=interval,
        aggregation=None,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        resource=resource2,
    )

    # Query the metrics
    time_series1 = client.list_time_series(request=request1)
    time_series2 = client.list_time_series(request=request2)
    return time_series1, time_series2
