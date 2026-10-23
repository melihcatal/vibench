import time
from google.cloud import monitoring_v3
from google.cloud.monitoring_v3.types import TimeInterval
from google.protobuf.timestamp_pb2 import Timestamp
from typing import Dict, List, Optional

from observability_client import get_monitoring_client, get_project_id


def get_series(client, project_name, metric_name, dimensions, interval):
    dimension_filters = " AND ".join(
        [f'metric.labels.{key} = "{value}"' for key, value in dimensions.items()]
    )
    filter_string = f'metric.type = "{metric_name}" AND {dimension_filters}'

    request = {
        "name": project_name,
        "filter": filter_string,
        "interval": interval,
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    }

    response = client.list_time_series(request)
    return list(response)


def compare_metric_series(
    metric_name: str,
    dimensions1: Dict[str, str],
    dimensions2: Dict[str, str],
    minutes_ago: int = 60,
) -> Dict:
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

    series1 = get_series(client, project_name, metric_name, dimensions1, interval)
    series2 = get_series(client, project_name, metric_name, dimensions2, interval)

    comparison = {
        "series1_count": len(series1),
        "series2_count": len(series2),
        "series1_points": [len(s.points) for s in series1],
        "series2_points": [len(s.points) for s in series2],
    }
    return comparison
