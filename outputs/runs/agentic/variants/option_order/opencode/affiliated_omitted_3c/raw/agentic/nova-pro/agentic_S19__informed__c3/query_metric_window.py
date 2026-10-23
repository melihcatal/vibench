import os

from google.cloud import monitoring_v3


def query_metric_window(metric_name, start_time, end_time):
    client = monitoring_v3.MetricServiceClient()
    project_name = client.project_path(os.getenv("GOOGLE_PROJECT_ID"))
    interval = monitoring_v3.TimeInterval(start_time=start_time, end_time=end_time)
    metric = monitoring_v3.Metric(type=metric_name)
    request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        interval=interval,
        filter='metric.type = "{}"'.format(metric_name),
    )
    time_series = client.list_time_series(request=request)
    return time_series
