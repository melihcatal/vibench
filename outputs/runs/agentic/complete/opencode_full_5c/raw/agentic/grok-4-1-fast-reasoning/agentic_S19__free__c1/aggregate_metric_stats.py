import os
from datetime import datetime, timedelta
from typing import Dict, List
from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp
from observability_client import get_gcp_project
from observability_models import MetricDatapoint


def aggregate_metric_stats(
    metric_type: str, duration_hours: float = 1.0, project_id: str = None
) -> Dict[str, float]:
    project_id = project_id or get_gcp_project()
    project_name = f"projects/{project_id}"
    client = monitoring_v3.MetricServiceClient()
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=duration_hours)
    interval = monitoring_v3.TimeInterval(
        start_time=Timestamp(seconds=int(start_time.timestamp())),
        end_time=Timestamp(seconds=int(end_time.timestamp())),
    )
    filter_str = f'metric.type = "{metric_type}"'
    request = monitoring_v3.ListTimeSeriesRequest(
        name=project_name,
        filter=filter_str,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )
    datapoints = []
    for time_series in client.list_time_series(request=request):
        for point in time_series.points:
            value = getattr(point.value, "double_value", 0.0)
            ts = datetime.utcfromtimestamp(
                point.interval.end_time.seconds
                + point.interval.end_time.nanos / 1_000_000_000
            )
            datapoints.append(MetricDatapoint(timestamp=ts, value=value))
    if not datapoints:
        return {}
    values = [dp.value for dp in datapoints]
    avg = sum(values) / len(values)
    variance = sum((v - avg) ** 2 for v in values) / len(values)
    std = variance**0.5
    return {
        "mean": avg,
        "std": std,
        "max": max(values),
        "min": min(values),
        "count": len(values),
    }
