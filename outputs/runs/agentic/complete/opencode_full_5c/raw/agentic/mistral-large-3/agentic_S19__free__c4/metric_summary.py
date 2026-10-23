import os
from typing import Dict, List
from datetime import datetime, timedelta

from observability_client import ObservabilityClient
from observability_models import MetricPoint, MetricStats


def summarize_recent_trends(
    metric_type: str, hours: int = 24, threshold: float = 1.5
) -> Dict:
    """Summarize recent metric trends or anomalies using Google Cloud Monitoring."""
    client = ObservabilityClient()
    interval = client.build_time_interval(hours)
    filter_str = client.build_metric_filter(metric_type)

    result = client.client.list_time_series(
        name=client.project_name,
        filter=filter_str,
        interval=interval,
        aggregation={
            "alignment_period": {"seconds": 3600},
            "per_series_aligner": 1,  # ALIGN_MEAN
        },
    )

    if not result:
        return {"trend": "stable", "anomalies": [], "stats": None}

    points = []
    for ts in result:
        for point in ts.points:
            points.append(
                MetricPoint(
                    timestamp=datetime.fromtimestamp(
                        point.interval.end_time.timestamp(), datetime.timezone.utc
                    ),
                    value=point.value.double_value,
                    labels=ts.resource.labels,
                )
            )

    if len(points) < 2:
        return {"trend": "insufficient_data", "anomalies": [], "stats": None}

    values = [p.value for p in points]
    mean = sum(values) / len(values)
    anomalies = [
        {
            "timestamp": p.timestamp.isoformat(),
            "value": p.value,
            "deviation": abs(p.value - mean) / mean,
        }
        for p in points
        if abs(p.value - mean) / mean > threshold
    ]

    trend = (
        "increasing"
        if values[-1] > values[0] * 1.1
        else "decreasing"
        if values[-1] < values[0] * 0.9
        else "stable"
    )

    return {
        "trend": trend,
        "anomalies": anomalies,
        "stats": MetricStats(
            count=len(values),
            mean=mean,
            min=min(values),
            max=max(values),
            sum=sum(values),
        ),
    }
