from __future__ import annotations

from datetime import timedelta

from observability_models import MetricWindowRequest
from query_metric_window import query_metric_window


def metric_summary(metric_name: str, namespace: str, minutes: int = 60):
    end_time = __import__("datetime").datetime.now(__import__("datetime").timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)
    request = MetricWindowRequest(metric_name=metric_name, namespace=namespace, start_time=start_time, end_time=end_time)
    series = query_metric_window(request)
    values = [point.value for point in series.datapoints]
    if not values:
        return {"metric_name": metric_name, "namespace": namespace, "trend": "no-data", "anomaly": False}
    average = sum(values) / len(values)
    latest = values[-1]
    deviation = abs(latest - average) / average if average else 0.0
    return {"metric_name": metric_name, "namespace": namespace, "trend": "rising" if latest >= average else "falling", "anomaly": deviation > 0.5}
