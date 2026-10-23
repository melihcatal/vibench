from __future__ import annotations

from datetime import datetime
from typing import Dict, Optional

from observability_client import CloudWatchMetricsClient
from observability_models import MetricSeries, window_from_minutes


AWS_PROVIDER_SIGNAL = "boto3.cloudwatch"


def filter_metric_dimensions(metric_name: str, dimensions: Dict[str, str], minutes: int = 60, granularity: int = 60, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None) -> MetricSeries:
    client = CloudWatchMetricsClient()
    if start_time is None or end_time is None:
        start_time, end_time = window_from_minutes(minutes)
    return client.filter_metric_dimensions(metric_name=metric_name, dimensions=dimensions, start_time=start_time, end_time=end_time, period=granularity)
