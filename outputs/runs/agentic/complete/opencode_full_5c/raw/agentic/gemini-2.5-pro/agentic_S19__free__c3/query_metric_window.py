import time
from datetime import datetime, timedelta
from google.protobuf.timestamp_pb2 import Timestamp
from observability_client import get_monitoring_client, get_project_id
from observability_models import MetricData, TimeSeriesPoint


def query_metric_window(metric_name: str, minutes: int = 60) -> MetricData:
    client = get_monitoring_client()
    project_id = get_project_id()
    project_name = f"projects/{project_id}"

    now = time.time()
    seconds = int(now)
    nanos = int((now - seconds) * 10**9)

    interval = monitoring_v3.TimeInterval(
        {
            "end_time": Timestamp(seconds=seconds, nanos=nanos),
            "start_time": Timestamp(seconds=seconds - (minutes * 60), nanos=nanos),
        }
    )

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": f'metric.type = "{metric_name}"',
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    points = []
    for result in results:
        for point in result.points:
            points.append(
                TimeSeriesPoint(
                    timestamp=point.interval.start_time.timestamp(),
                    value=point.value.double_value,
                )
            )

    return MetricData(metric_name=metric_name, points=points)
