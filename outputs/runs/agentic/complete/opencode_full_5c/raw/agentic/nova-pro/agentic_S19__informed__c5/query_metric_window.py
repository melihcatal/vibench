import os

from google.cloud import monitoring_v3


def query_metric_window(metric_name, start_time, end_time):
    client = monitoring_v3.MetricServiceClient()
    project_name = client.project_path(os.getenv("GOOGLE_CLOUD_PROJECT"))
    filter = f'metric.type = "{metric_name}"'
    interval = monitoring_v3.TimeInterval(start_time=start_time, end_time=end_time)
    request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name, filter=filter, interval=interval
    )
    response = client.list_time_series(request)
    return response
