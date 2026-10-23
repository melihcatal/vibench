import os
from google.cloud import monitoring_v3
from google.protobuf import timestamp_pb2

def query_metric_window(project_id: str, metric_type: str, end_time: int, minutes_ago: int):
    client = monitoring_v3.MetricServiceClient()
    project_name = f"projects/{project_id}"

    now = timestamp_pb2.Timestamp()
    now.seconds = end_time
    
    interval = monitoring_v3.TimeInterval(
        end_time=now,
        start_time=timestamp_pb2.Timestamp(seconds=now.seconds - (minutes_ago * 60)),
    )

    query = f"""
    fetch gce_instance
    | metric {metric_type}
    | align delta(1m)
    | every 1m
    | group_by [], [value_mean: mean(value.double_value)]
    """

    results = client.query_time_series(
        name=project_name,
        query=query,
        interval=interval,
    )

    return results

