from typing import Dict, List, Optional
from observability_client import ObservabilityClient
from observability_models import MetricSeries, normalize_gcp_metric_response
import numpy as np


def summarize_metric_trends(
    metric_type: str, hours: int = 24, filter_str: str = None, threshold: float = 2.0
) -> Dict:
    client = ObservabilityClient()
    interval = client.build_time_interval(hours)

    request = {
        "name": client.project_name,
        "filter": f'metric.type="{metric_type}"'
        + (f" AND {filter_str}" if filter_str else ""),
        "interval": interval,
        "view": "FULL",
    }

    response = client.client.list_time_series(request=request)
    series_list = normalize_gcp_metric_response(response)

    if not series_list:
        return {"trend": "stable", "anomalies": [], "stats": {}}

    series = series_list[0]
    values = [point.value for point in series.points]
    timestamps = [point.timestamp for point in series.points]

    mean = np.mean(values)
    std = np.std(values)
    anomalies = []

    for point in series.points:
        z_score = (point.value - mean) / std if std != 0 else 0
        if abs(z_score) > threshold:
            anomalies.append(
                {
                    "timestamp": point.timestamp,
                    "value": point.value,
                    "z_score": z_score,
                    "labels": point.labels,
                }
            )

    trend = (
        "increasing"
        if len(anomalies) > 0 and all(a["z_score"] > 0 for a in anomalies)
        else "decreasing"
        if len(anomalies) > 0 and all(a["z_score"] < 0 for a in anomalies)
        else "stable"
    )

    return {
        "trend": trend,
        "anomalies": anomalies,
        "stats": {
            "mean": mean,
            "stddev": std,
            "min": min(values),
            "max": max(values),
        },
    }
