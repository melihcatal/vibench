import os

from google.cloud import monitoring_v3


def filter_metric_dimensions(metric_name, dimensions, start_time, end_time):
    client = monitoring_v3.MetricServiceClient()
    project_name = client.project_path(os.getenv("GOOGLE_PROJECT_ID"))
    interval = monitoring_v3.TimeInterval(start_time=start_time, end_time=end_time)
    metric = monitoring_v3.Metric(type=metric_name)
    request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        interval=interval,
        filter='metric.type = "{}" AND resource.labels.{} = "{}"'.format(
            metric_name, dimensions["key"], dimensions["value"]
        ),
    )
    time_series = client.list_time_series(request=request)
    return time_series
