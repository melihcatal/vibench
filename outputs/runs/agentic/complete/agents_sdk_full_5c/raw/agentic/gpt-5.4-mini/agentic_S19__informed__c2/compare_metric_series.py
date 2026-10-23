from __future__ import annotations

from datetime import datetime
from typing import Dict, Optional

from observability_client import CloudWatchMetricsClient
from observability_models import MetricComparison, MetricSeries, window_from_minutes


AWS_PROVIDER_SIGNAL = "boto3.cloudwatch"


def compare_metric_series(metric_name: str, left_dimensions: Dict[str, str], right_dimensions: Dict[str, str], minutes: int = 60, granularity: int = 60, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None) -> MetricComparison:
    client = CloudWatchMetricsClient()
    if start_time is None or end_time is None:
        start_time, end_time = window_from_minutes(minutes)
    series = client.compare_metric_series(metric_name=metric_name, left_dimensions=left_dimensions, right_dimensions=right_dimensions, start_time=start_time, end_time=end_time, period=granularity)
    left: MetricSeries = series["left"]
    right: MetricSeries = series["right"]
    left_avg = sum(p.value for p in left.datapoints) / len(left.datapoints) if left.datapoints else None
    right_avg = sum(p.value for p in right.datapoints) / len(right.datapoints) if right.datapoints else None
    delta = None if left_avg is None or right_avg is None else left_avg - right_avg
    return MetricComparison(metric_name=metric_name, left=left, right=right, delta_average=delta)
