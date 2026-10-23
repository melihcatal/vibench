from __future__ import annotations

from statistics import mean

from observability_models import MetricSummary, MetricWindowRequest
from query_metric_window import query_metric_window


def metric_summary(request: MetricWindowRequest) -> MetricSummary:
    response = query_metric_window(request)
    values = [point.value for point in response.points if point.value is not None]
    if not values:
        return MetricSummary(
            metric_type=request.metric_type,
            sample_count=0,
            average=None,
            minimum=None,
            maximum=None,
            trend="no_data",
            anomaly_detected=False,
        )
    midpoint = max(1, len(values) // 2)
    first_half = values[:midpoint]
    second_half = values[midpoint:]
    first_avg = mean(first_half)
    second_avg = mean(second_half) if second_half else first_avg
    change_ratio = 0.0 if first_avg == 0 else (second_avg - first_avg) / abs(first_avg)
    trend = "stable"
    if change_ratio > 0.1:
        trend = "up"
    elif change_ratio < -0.1:
        trend = "down"
    avg = mean(values)
    anomaly_detected = any(abs(v - avg) > max(abs(avg) * 0.5, 1.0) for v in values)
    return MetricSummary(
        metric_type=request.metric_type,
        sample_count=len(values),
        average=avg,
        minimum=min(values),
        maximum=max(values),
        trend=trend,
        anomaly_detected=anomaly_detected,
    )
