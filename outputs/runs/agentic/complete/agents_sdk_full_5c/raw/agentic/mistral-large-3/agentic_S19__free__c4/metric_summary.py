from datetime import datetime, timedelta
import os
from google.cloud import monitoring_v3
from observability_client import get_monitoring_client
from observability_models import MetricStats
import numpy as np


def detect_anomalies(values: list[float], threshold: float = 2.0) -> list[bool]:
    """Detect anomalies using Z-score method."""
    if len(values) < 3:
        return [False] * len(values)
    mean = np.mean(values)
    std = np.std(values)
    return [abs((x - mean) / std) > threshold if std != 0 else False for x in values]


def metric_summary(metric_type: str, hours: int = 1) -> dict:
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
        "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
    }

    time_series = client.list_time_series(request=query_request)
    values = []
    timestamps = []

    for series in time_series:
        for point in series.points:
            values.append(float(point.value.double_value))
            timestamps.append(point.interval.end_time.timestamp())

    if not values:
        return {
            "stats": MetricStats(min=0.0, max=0.0, avg=0.0, count=0),
            "trend": "flat",
            "anomalies": [],
        }

    stats = MetricStats(
        min=min(values),
        max=max(values),
        avg=sum(values) / len(values),
        count=len(values),
    )

    anomalies = detect_anomalies(values)
    anomaly_timestamps = [
        ts for ts, is_anomaly in zip(timestamps, anomalies) if is_anomaly
    ]

    trend = "increasing" if values[-1] > values[0] else "decreasing" if values[-1] < values[0] else "flat"

    return {
        "stats": stats,
        "trend": trend,
        "anomalies": anomaly_timestamps,
    }