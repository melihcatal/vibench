from google.cloud import monitoring_v3
from observability_client import ObservabilityClient
from observability_models import MetricNormalizer
from typing import List, Dict, Optional


def summarize_metric_trends(metric_name: str, hours: int = 24) -> Dict:
    """Summarize recent metric trends or anomalies using Google Cloud Monitoring."""
    client = ObservabilityClient()
    interval = client.build_time_interval(hours)

    query = f'metric.type="{metric_name}"'
    result = client.client.list_time_series(
        name=client.project_name,
        filter=query,
        interval=interval,
        view=monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    )

    series = [MetricNormalizer.normalize_series(s) for s in result]
    if not series:
        return {"metric": metric_name, "trend": "no_data", "anomalies": []}

    points = [point for s in series for point in s.points]
    if len(points) < 2:
        return {"metric": metric_name, "trend": "insufficient_data", "anomalies": []}

    values = [p.value for p in points]
    timestamps = [p.timestamp for p in points]
    mean = sum(values) / len(values)
    stddev = (sum((x - mean) ** 2 for x in values) / len(values)) ** 0.5

    anomalies = [
        {
            "timestamp": p.timestamp.isoformat(),
            "value": p.value,
            "deviation": (p.value - mean) / stddev,
        }
        for p in points
        if abs(p.value - mean) > 2 * stddev
    ]

    trend = "stable"
    if values[-1] > values[0] * 1.2:
        trend = "increasing"
    elif values[-1] < values[0] * 0.8:
        trend = "decreasing"

    return {
        "metric": metric_name,
        "trend": trend,
        "anomalies": anomalies,
        "stats": {
            "mean": mean,
            "stddev": stddev,
            "min": min(values),
            "max": max(values),
        },
    }
