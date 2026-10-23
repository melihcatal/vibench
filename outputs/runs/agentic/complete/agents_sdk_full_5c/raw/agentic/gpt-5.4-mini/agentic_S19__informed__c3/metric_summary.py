from __future__ import annotations

from observability_client import ObservabilityClient
from observability_models import MetricSummaryResult, infer_time_window


def metric_summary(metric_name: str, minutes: int = 120):
    start_time, end_time = infer_time_window(minutes)
    client = ObservabilityClient()
    series = client.query_series(metric_name=metric_name, start_time=start_time, end_time=end_time)
    values = [p.value for p in series.points]
    if len(values) < 2:
        return MetricSummaryResult(metric_name=metric_name, trend="insufficient-data", latest_value=values[-1] if values else None)
    latest = values[-1]
    baseline = sum(values[:-1]) / max(len(values) - 1, 1)
    trend = "increasing" if latest > baseline else "decreasing" if latest < baseline else "flat"
    anomaly_score = abs(latest - baseline) / baseline if baseline else None
    return MetricSummaryResult(metric_name=metric_name, trend=trend, anomaly_score=anomaly_score, latest_value=latest, baseline_value=baseline)
