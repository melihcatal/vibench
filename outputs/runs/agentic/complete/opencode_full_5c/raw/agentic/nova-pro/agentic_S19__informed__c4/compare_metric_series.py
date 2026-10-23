import os

from google.cloud import monitoring_v3


def compare_metric_series(
    metric_name, resource_filter1, resource_filter2, start_time, end_time
):
    client = monitoring_v3.MetricServiceClient()
    project_name = client.project_path(os.getenv("GCP_PROJECT_ID"))
    filter1 = f'metric.type = "{metric_name}" AND {resource_filter1}'
    filter2 = f'metric.type = "{metric_name}" AND {resource_filter2}'
    interval = monitoring_v3.TimeInterval(start_time=start_time, end_time=end_time)
    request1 = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=filter1,
        interval=interval,
    )
    request2 = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=filter2,
        interval=interval,
    )
    time_series1 = client.list_time_series(request1)
    time_series2 = client.list_time_series(request2)
    return time_series1, time_series2
