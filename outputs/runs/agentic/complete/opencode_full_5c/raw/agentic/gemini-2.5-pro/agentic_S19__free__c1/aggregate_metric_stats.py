import time
from google.cloud.monitoring_v3.types import TimeInterval, Aggregation
from google.protobuf.timestamp_pb2 import Timestamp

from observability_client import get_monitoring_client, get_project_id


def get_aggregated_stats(
    metric_name: str, minutes_ago: int = 60, alignment_period_seconds: int = 600
) -> list:
    client = get_monitoring_client()
    project_id = get_project_id()
    project_name = f"projects/{project_id}"

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)

    interval = TimeInterval(
        end_time=Timestamp(seconds=seconds, nanos=nanos),
        start_time=Timestamp(seconds=(seconds - minutes_ago * 60), nanos=nanos),
    )

    aggregation = Aggregation(
        alignment_period={"seconds": alignment_period_seconds},
        per_series_aligner=Aggregation.Aligner.ALIGN_MEAN,
        cross_series_reducer=Aggregation.Reducer.REDUCE_SUM,
        group_by_fields=["metric.label.instance_name"],
    )

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": f'metric.type = "{metric_name}"',
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
            "aggregation": aggregation,
        }
    )

    aggregated_data = []
    for result in results:
        if result.points:
            point = result.points[0]  # Aggregated to a single point
            data = {
                "metric": result.metric.type,
                "labels": dict(result.metric.labels),
                "value": point.value.double_value,
            }
            aggregated_data.append(data)

    return aggregated_data
