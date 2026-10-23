import time
from google.cloud.monitoring_v3.types import TimeInterval
from google.protobuf.timestamp_pb2 import Timestamp

from observability_client import get_monitoring_client, get_project_id
from observability_models import MetricTimeSeries, TimeSeriesPoint


def query_metric_window(
    metric_name: str, minutes_ago: int = 60
) -> list[MetricTimeSeries]:
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

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": f'metric.type = "{metric_name}"',
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    time_series_list = []
    for result in results:
        points = []
        for point in result.points:
            points.append(
                TimeSeriesPoint(
                    timestamp=point.interval.end_time.isoformat(),
                    value=point.value.double_value,
                )
            )

        dimensions = {
            label: result.metric.labels[label] for label in result.metric.labels
        }
        time_series_list.append(
            MetricTimeSeries(
                metric_name=result.metric.type,
                dimensions=dimensions,
                points=points,
            )
        )
    return time_series_list
