from __future__ import annotations

from observability_client import ObservabilityClient
from observability_models import MetricComparisonResult, infer_time_window


def compare_metric_series(metric_name: str, left_filter: dict[str, str], right_filter: dict[str, str], minutes: int = 60):
    start_time, end_time = infer_time_window(minutes)
    client = ObservabilityClient()
    left, right = client.compare_series(metric_name=metric_name, left_dimensions=left_filter, right_dimensions=right_filter, start_time=start_time, end_time=end_time)
    left_values = [p.value for p in left.points]
    right_values = [p.value for p in right.points]
    left_avg = sum(left_values) / len(left_values) if left_values else None
    right_avg = sum(right_values) / len(right_values) if right_values else None
    delta = (left_avg - right_avg) if left_avg is not None and right_avg is not None else None
    ratio = (left_avg / right_avg) if left_avg is not None and right_avg not in (None, 0) else None
    return MetricComparisonResult(metric_name=metric_name, left_label=str(left_filter), right_label=str(right_filter), left_average=left_avg, right_average=right_avg, delta=delta, ratio=ratio)
