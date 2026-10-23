# LATER-STEP
# metric_summary.py
# Summarize recent metric trends or anomalies using Datadog as the managed metrics provider

from datetime import datetime, timedelta
from observability_client import get_datadog_client
from observability_models import MetricStatsRequest, MetricStatsResponse


def summarize_recent_trends(metric: str, hours: int = 24) -> dict:
    """
    Produce a concise summary of a metric's recent behavior.

    Includes average, max, min, total, count and optional anomaly detection flag.

    Args:
        metric (str): Datadog metric name, e.g., "system.cpu.user".
        hours (int): Lookback window in hours (default 24).

    Returns:
        dict: Summary fields with human‑readable keys.
    """
    end = datetime.utcnow().isoformat() + "Z"
    start = (datetime.utcnow() - timedelta(hours=hours)).isoformat() + "Z"
    client = get_datadog_client()
    request = MetricStatsRequest(query=metric, start=start, end=end, interval=60)
    raw = client.aggregate_metrics(request)  # Datadog API call
    stats = MetricStatsResponse.from_dict(raw).statistics
    # Simple anomaly heuristics: flag if max > 2 * avg
    anomaly = "high" if stats.get("max", 0) > 2 * stats.get("avg", 0) else "normal"
    return {
        "metric": metric,
        "window": f"{hours}h",
        "avg": round(stats.get("avg", 0), 3),
        "max": round(stats.get("max", 0), 3),
        "min": round(stats.get("min", 0), 3),
        "sum": round(stats.get("sum", 0), 3),
        "count": int(stats.get("count", 0)),
        "anomaly": anomaly,
    }
