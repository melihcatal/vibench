import os

from google.cloud import monitoring_v3


def aggregate_metric_stats(metric_name, start_time, end_time):
    client = monitoring_v3.MetricServiceClient()
    project_name = client.project_path(os.getenv("GCP_PROJECT_ID"))
    filter = f'metric.type = "{metric_name}"'
    interval = monitoring_v3.TimeInterval(start_time=start_time, end_time=end_time)
    aggregation = monitoring_v3.Aggregation(
        alignment_period=monitoring_v3.Duration(seconds=60),
        per_series_aligner=monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
    )
    request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=filter,
        interval=interval,
        aggregation=aggregation,
    )
    time_series = client.list_time_series(request)
    return time_series
