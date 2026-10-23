from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2

def filter_metric_dimensions(project_id: str, metric_type: str, resource_type: str, resource_labels: dict, metric_labels: dict, start_time_seconds: int, end_time_seconds: int):
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = timestamp_pb2.Timestamp()
    now.seconds = end_time_seconds

    five_minutes_ago = timestamp_pb2.Timestamp()
    five_minutes_ago.seconds = start_time_seconds

    interval = monitoring_v3.TimeInterval(end_time=now, start_time=five_minutes_ago)

    query_filter = f'metric.type = "{metric_type}" AND resource.type = "{resource_type}"'

    for label_key, label_value in resource_labels.items():
        query_filter += f' AND resource.labels.{label_key} = "{label_value}"'

    for label_key, label_value in metric_labels.items():
        query_filter += f' AND metric.labels.{label_key} = "{label_value}"'

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": query_filter,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    return results
