# [SAME-SCENARIO] aggregate_metric_stats.py

# Retrieve aggregated statistics for a metric over a time window.
# Provider: Amazon CloudWatch Metrics (boto3 SDK)

import os
from datetime import datetime, timedelta
from typing import List, Dict, Any

from .observability_client import get_cloudwatch_client
from .observability_models import CloudWatchMetricStatQuery, normalize_metric_response


def aggregate_metric_stats(
    metric_name: str,
    namespace: str = "AWS/EC2",
    window_minutes: int = 60,
    period: int = 60,
    statistics: List[str] = ["Average", "Minimum", "Maximum", "Sum", "SampleCount"],
    dimensions: List[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """
    Retrieves aggregated statistics for *metric_name* in the given *namespace*
    over the last *window_minutes*.

    Returns a list of raw CloudWatch aggregate dicts (each containing Label, Value, Unit).
    """
    client = get_cloudwatch_client()
    end = datetime.utcnow()
    start = end - timedelta(minutes=window_minutes)
    query = CloudWatchMetricStatQuery(
        namespace=namespace,
        metric_name=metric_name,
        start_time=start.isoformat() + "Z",
        end_time=end.isoformat() + "Z",
        period=period,
        statistics=statistics,
        dimensions=dimensions,
    )
    api_params = {
        "Namespace": query.namespace,
        "MetricName": query.metric_name,
        "StartTime": query.start_time,
        "EndTime": query.end_time,
        "Period": query.period,
        "Statistics": query.statistics,
        "Dimensions": query.dimensions,
    }
    try:
        raw_resp = client.get_metric_statistics(**api_params)
    except Exception as exc:
        raise RuntimeError(f"CloudWatch stats query failed for {metric_name}") from exc
    return normalize_metric_response(raw_resp)
