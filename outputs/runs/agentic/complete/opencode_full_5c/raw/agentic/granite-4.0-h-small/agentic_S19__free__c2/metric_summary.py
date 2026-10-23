# [LATER-STEP] metric_summary.py

from observability_client import metrics_path
from observability_models import (
    MetricQueryRequest,
    MetricQueryResponse,
    normalize_series,
)

import datetime

# Example provider‑specific request for a metric summary


def metric_summary(metric_name, start_window="-30m", end_window="now"):
    # Build a request that fetches recent data and requests aggregation
    request = MetricQueryRequest(
        metric=metric_name,
        start=start_window,
        end=end_window,
        aggregation="ALIGN_DELTA",  # provider‑specific aggregation type
    )
    # The client uses the concrete Google Cloud Monitoring SDK
    response = MetricsClient().query(request)
    # Normalize the raw series into a simple list of dicts
    series = normalize_series(response.series)
    # Simple summarization logic (e.g., detect trend direction)
    if not series:
        return {"metric": metric_name, "summary": "No data"}
    # Example: compute basic trend from the last few points
    points = series[0]["points"][-5:]  # last 5 points
    timestamps = [pt["interval"]["end_time"] for pt in points]
    values = [pt["value"]["doubleValue"] for pt in points]
    trend = "stable"
    if values[-1] > values[0]:
        trend = "rising"
    elif values[-1] < values[0]:
        trend = "falling"
    return {
        "metric": metric_name,
        "summary": f"Recent trend is {trend}",
        "last_point": {"timestamp": timestamps[-1], "value": values[-1]},
    }
