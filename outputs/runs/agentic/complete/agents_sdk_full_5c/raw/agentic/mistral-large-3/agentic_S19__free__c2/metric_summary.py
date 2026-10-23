from datetime import datetime, timedelta
import os
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client
from observability_models import MetricStats


def detect_anomalies(metric_type: str, hours: int = 1, threshold: float = 2.0) -> dict:
    """Summarize recent metric trends or anomalies using Google Cloud Monitoring."""
    client = get_monitoring_client()
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable must be set.")

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours)

    query_request = {
        "name": f"projects/{project_id}",
        "filter": f'metric.type="{metric_type}"',
        "interval": {
            "start_time": {"seconds": int(start_time.timestamp())},
            "end_time": {"seconds": int(end_time.timestamp())},
        },
        "aggregation": {
            "alignment_period": {"seconds": 300},
            "per_series_aligner": monitoring_v3.Aggregation.Aligner.ALIGN_MEAN,
        },
    }

    time_series = list(client.list_time_series(request=query_request))
    stats = MetricStats()
    anomalies = []

    for series in time_series:
        values = [point.value.double_value for point in series.points]
        if not values:
            continue

        avg = sum(values) / len(values)
        std_dev = (sum((x - avg) ** 2 for x in values) / len(values)) ** 0.5

        for point in series.points:
            value = point.value.double_value
            if abs(value - avg) > threshold * std_dev:
                anomalies.append({
                    "timestamp": point.interval.end_time.timestamp(),
                    "value": value,
                    "expected_range": (avg - threshold * std_dev, avg + threshold * std_dev),
                })

        stats.count += len(values)
        stats.sum += sum(values)
        stats.min = min(stats.min, min(values))
        stats.max = max(stats.max, max(values))

    if stats.count > 0:
        stats.avg = stats.sum / stats.count

    return {
        "stats": stats,
        "anomalies": anomalies,
        "trend": "increasing" if stats.max > stats.avg * 1.2 else "stable" if stats.max < stats.avg * 1.1 else "decreasing",
    }