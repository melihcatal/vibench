from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

from google.cloud import monitoring_v3

from observability_client import load_config, metric_client
from observability_models import MetricCompareRequest


def _series_values(series) -> List[float]:
    values: List[float] = []
    for ts in series:
        for point in ts.points:
            val = point.value.double_value or point.value.int64_value or point.value.distribution_value.count
            values.append(float(val))
    return values


def compare_metric_series(request: MetricCompareRequest) -> Dict[str, Any]:
    config = load_config()
    client = metric_client()
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=request.minutes)
    interval = monitoring_v3.TimeInterval({"end_time": end_time, "start_time": start_time})

    left = client.list_time_series(request={"name": f"projects/{config.project_id}", "filter": request.left_filter or f'metric.type = "{request.metric_type}"', "interval": interval, "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL})
    right = client.list_time_series(request={"name": f"projects/{config.project_id}", "filter": request.right_filter or f'metric.type = "{request.metric_type}"', "interval": interval, "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL})

    left_values = _series_values(left)
    right_values = _series_values(right)
    return {
        "metric_type": request.metric_type,
        "left_mean": sum(left_values) / len(left_values) if left_values else None,
        "right_mean": sum(right_values) / len(right_values) if right_values else None,
        "delta": ((sum(left_values) / len(left_values)) - (sum(right_values) / len(right_values))) if left_values and right_values else None,
    }
