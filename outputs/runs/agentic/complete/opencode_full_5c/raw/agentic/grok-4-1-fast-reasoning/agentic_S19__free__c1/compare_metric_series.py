import os
from datetime import datetime, timedelta
from typing import Dict, Any, List
from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp
from observability_client import get_gcp_project
from observability_models import MetricDatapoint


def compare_metric_series(
    metric_type: str,
    dimensions1: Dict[str, str],
    dimensions2: Dict[str, str],
    duration_hours: float = 1.0,
    project_id: str = None,
) -> Dict[str, Any]:
    project_id = project_id or get_gcp_project()
    project_name = f"projects/{project_id}"
    client = monitoring_v3.MetricServiceClient()
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=duration_hours)
    interval = monitoring_v3.TimeInterval(
        start_time=Timestamp(seconds=int(start_time.timestamp())),
        end_time=Timestamp(seconds=int(end_time.timestamp())),
    )

    def get_datapoints(dims: Dict[str, str]) -> List[MetricDatapoint]:
        filter_parts = [f'metric.type = "{metric_type}"']
        for key, value in dims.items():
            filter_parts.append(f'{key} = "{value}"')
        filter_str = " AND ".join(filter_parts)
        request = monitoring_v3.ListTimeSeriesRequest(
            name=project_name,
            filter=filter_str,
            interval=interval,
            view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
        )
        dps = []
        for time_series in client.list_time_series(request=request):
            for point in time_series.points:
                value = getattr(point.value, "double_value", 0.0)
                ts = datetime.utcfromtimestamp(
                    point.interval.end_time.seconds
                    + point.interval.end_time.nanos / 1_000_000_000
                )
                dps.append(MetricDatapoint(timestamp=ts, value=value))
        return dps

    dps1 = get_datapoints(dimensions1)
    dps2 = get_datapoints(dimensions2)
    if not dps1 or not dps2:
        return {"error": "No data for one or both series"}
    avg1 = sum(dp.value for dp in dps1) / len(dps1)
    avg2 = sum(dp.value for dp in dps2) / len(dps2)
    return {
        "avg_series1": avg1,
        "avg_series2": avg2,
        "difference": avg1 - avg2,
        "ratio": avg1 / avg2 if avg2 != 0 else float("inf"),
    }
