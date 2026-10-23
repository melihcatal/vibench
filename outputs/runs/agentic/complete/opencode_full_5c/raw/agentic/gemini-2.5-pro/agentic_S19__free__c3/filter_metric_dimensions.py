import time
from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp
from observability_client import get_monitoring_client, get_project_id
from observability_models import MetricData, TimeSeriesPoint
from typing import Dict, List


def filter_metric_by_dimensions(
    metric_name: str, dimensions: Dict[str, str], minutes: int = 60
) -> List[MetricData]:
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

    filter_str = f'metric.type = "{metric_name}"'
    for key, value in dimensions.items():
        filter_str += f' AND metric.label.{key} = "{value}"'

    results = client.list_time_series(
        request={
            "name": project_name,
            "filter": filter_str,
            "interval": interval,
            "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        }
    )

    series_list = []
    for result in results:
        points = []
        for point in result.points:
            points.append(
                TimeSeriesPoint(
                    timestamp=point.interval.start_time.timestamp(),
                    value=point.value.double_value,
                )
            )

        series_dimensions = {
            label: value for label, value in result.metric.labels.items()
        }

        series_list.append(
            MetricData(
                metric_name=metric_name,
                points=points,
                dimensions=series_dimensions,
            )
        )
    return series_list
