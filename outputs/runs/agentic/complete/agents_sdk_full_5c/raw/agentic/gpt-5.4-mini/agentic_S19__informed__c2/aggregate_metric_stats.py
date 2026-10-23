from __future__ import annotations

from datetime import datetime
from typing import Dict, Optional

from observability_client import CloudWatchMetricsClient
from observability_models import MetricQuery, MetricStats, window_from_minutes


AWS_PROVIDER_SIGNAL = "boto3.cloudwatch"


def aggregate_metric_stats(metric_name: str, minutes: int = 60, dimensions: Optional[Dict[str, str]] = None, granularity: int = 60, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None) -> MetricStats:
    client = CloudWatchMetricsClient()
    if start_time is None or end_time is None:
        start_time, end_time = window_from_minutes(minutes)
    query = MetricQuery(metric_name=metric_name, start_time=start_time, end_time=end_time, dimensions=dimensions or {}, granularity=granularity)
    return client.aggregate_metric_stats(query)
