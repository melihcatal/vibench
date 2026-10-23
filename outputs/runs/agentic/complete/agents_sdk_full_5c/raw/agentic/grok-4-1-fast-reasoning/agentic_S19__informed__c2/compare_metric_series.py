from datetime import datetime, timedelta
from google.cloud import monitoring_v3
from google.protobuf.timestamp_pb2 import Timestamp
import os
from typing import Dict
from observability_client import get_google_cloud_project
from observability_models import DataPoint

def _get_values(metric_name: str, filter_addition: str, window_hours: int):
    project_id = get_google_cloud_project()
    client = monitoring_v3.MetricServiceClient()
    end_time = Timestamp()
    end_time.GetCurrentTime()
    start_time = Timestamp()
    start_time.FromSeconds(int((datetime.utcnow() - timedelta(hours=window_hours)).timestamp()))
    interval = monitoring_v3.types.TimeInterval(start_time=start_time, end_time=end_time)
    filter_parts = [f'metric.type = "{metric_name}"']
    if filter_addition:
        filter_parts.append(filter_addition)
    filter_ = ' AND '.join(filter_parts)
    request = monitoring_v3.ListTimeSeriesRequest(
        name=f'projects/{project_id}',
        filter=filter_,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesView.FULL,
    )
    time_series_iter = client.list_time_series(request)
    values = []
    for time_series in time_series_iter:
        for point in time_series.points:
            if point.value.HasField('double_value'):
                values.append(point.value.double_value)
    return values

def compare_metric_series(metric_name: str, dimensions1: Dict[str, str], dimensions2: Dict[str, str], window_hours: int = 1) -> Dict[str, float]:
    filter1_parts = []
    for key, value in dimensions1.items():
        filter1_parts.append(f'resource.labels["{key}"] = "{value}"')
    filter1 = ' AND '.join(filter1_parts)
    values1 = _get_values(metric_name, filter1, window_hours)
    avg1 = sum(values1) / len(values1) if values1 else 0.0
    
    filter2_parts = []
    for key, value in dimensions2.items():
        filter2_parts.append(f'resource.labels["{key}"] = "{value}"')
    filter2 = ' AND '.join(filter2_parts)
    values2 = _get_values(metric_name, filter2, window_hours)
    avg2 = sum(values2) / len(values2) if values2 else 0.0
    
    diff_pct = ((avg1 - avg2) / avg2 * 100) if avg2 != 0 else float('inf')
    return {'avg1': avg1, 'avg2': avg2, 'diff_pct': diff_pct}
