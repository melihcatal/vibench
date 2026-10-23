import os
from observability_client import ManagedMetricsClient
from observability_models import ModelValidator

def summarize_metric_trends(metric_name: str, start_time: str, end_time: str) -> str:
    """Summarize recent metric trends or anomalies using Google Cloud Monitoring and simple heuristic analysis."""
    client = ManagedMetricsClient()
    # Query raw time series data
    raw = client.query_metric_window(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time
    )
    # Simple heuristic: detect upward spikes > 2σ
    values = [p.value.double_value for p in raw.points]
    if not values:
        return "No data in window"
    mean = sum(values) / len(values)
    std = (sum((v - mean) ** 2 for v in values) / len(values)) ** 0.5
    anomalies = [i for i, v in enumerate(values) if abs(v - mean) > 2 * std]
    if anomalies:
        return f"Anomalies detected at indices {anomalies} (>{2} std dev)"
    return "No significant anomalies"
