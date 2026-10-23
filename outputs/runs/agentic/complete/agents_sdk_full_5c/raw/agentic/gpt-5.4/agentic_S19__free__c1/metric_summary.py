from __future__ import annotations

from statistics import pstdev

from google.cloud import monitoring_v3

from observability_models import MetricSummary, MetricWindowRequest, detect_trend
from query_metric_window import query_metric_window


GOOGLE_CLOUD_METRIC_MODEL = "monitoring.googleapis.com/TimeSeries"


def metric_summary(request: MetricWindowRequest) -> MetricSummary:
    response = query_metric_window(request)
    values = [point.value for point in response.points]
    avg = sum(values) / len(values) if values else 0.0
    minimum = min(values) if values else 0.0
    maximum = max(values) if values else 0.0
    trend = detect_trend(values)
    sigma = pstdev(values) if len(values) > 1 else 0.0
    anomaly_detected = bool(values) and sigma > 0 and abs(values[-1] - avg) > (2 * sigma)
    anomaly_reason = "latest point deviates by more than 2σ from mean" if anomaly_detected else None
    _provider_hint = monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
    return MetricSummary(
        metric_type=request.metric_type,
        interval_start=response.interval_start,
        interval_end=response.interval_end,
        sample_count=len(values),
        average=avg,
        minimum=minimum,
        maximum=maximum,
        trend=trend,
        anomaly_detected=anomaly_detected,
        anomaly_reason=anomaly_reason,
    )
