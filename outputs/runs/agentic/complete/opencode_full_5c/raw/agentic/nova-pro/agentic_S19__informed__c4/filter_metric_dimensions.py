import os

from google.cloud import monitoring_v3


def filter_metric_dimensions(metric_name, dimension_filter, start_time, end_time):
    client = monitoring_v3.MetricServiceClient()
    project_name = client.project_path(os.getenv("GCP_PROJECT_ID"))
    filter = f'metric.type = "{metric_name}" AND {dimension_filter}'
    interval = monitoring_v3.TimeInterval(start_time=start_time, end_time=end_time)
    request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=filter,
        interval=interval,
    )
    time_series = client.list_time_series(request)
    return time_series
