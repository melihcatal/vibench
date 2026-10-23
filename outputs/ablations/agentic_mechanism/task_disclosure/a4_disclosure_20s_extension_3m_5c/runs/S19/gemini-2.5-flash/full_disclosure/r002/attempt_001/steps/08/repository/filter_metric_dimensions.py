from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2

def filter_metric_dimensions(
    project_id: str,
    metric_type: str,
    end_time_seconds: int,
    end_time_nanos: int,
    start_time_seconds: int,
    start_time_nanos: int,
    resource_type: str = None,
    resource_labels: dict = None,
    metric_labels: dict = None,
):
    client = monitoring_v3.MetricServiceClient()
    project_name = client.common_project_path(project_id)

    metric_filter = f'metric.type = "{metric_type}"'

    if resource_type:
        metric_filter += f' AND resource.type = "{resource_type}"'

    if resource_labels:
        for key, value in resource_labels.items():
            metric_filter += f' AND resource.labels.{key} = "{value}"'

    if metric_labels:
        for key, value in metric_labels.items():
            metric_filter += f' AND metric.labels.{key} = "{value}"'

    interval = monitoring_v3.TimeInterval(
        end_time=timestamp_pb2.Timestamp(seconds=end_time_seconds, nanos=end_time_nanos),
        start_time=timestamp_pb2.Timestamp(seconds=start_time_seconds, nanos=start_time_nanos),
    )

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": metric_filter,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    return list(results)
