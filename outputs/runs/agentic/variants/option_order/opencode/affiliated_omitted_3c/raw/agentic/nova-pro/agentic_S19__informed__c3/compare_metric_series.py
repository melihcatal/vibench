import os

from google.cloud import monitoring_v3


def compare_metric_series(metric_name, resource_a, resource_b, start_time, end_time):
    client = monitoring_v3.MetricServiceClient()
    project_name = client.project_path(os.getenv("GOOGLE_PROJECT_ID"))
    interval = monitoring_v3.TimeInterval(start_time=start_time, end_time=end_time)
    metric = monitoring_v3.Metric(type=metric_name)
    request_a = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        interval=interval,
        filter='metric.type = "{}" AND resource.labels.resource_id = "{}"'.format(
            metric_name, resource_a
        ),
    )
    request_b = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        interval=interval,
        filter='metric.type = "{}" AND resource.labels.resource_id = "{}"'.format(
            metric_name, resource_b
        ),
    )
    time_series_a = client.list_time_series(request=request_a)
    time_series_b = client.list_time_series(request=request_b)
    # Comparison logic here
    return comparison_result
