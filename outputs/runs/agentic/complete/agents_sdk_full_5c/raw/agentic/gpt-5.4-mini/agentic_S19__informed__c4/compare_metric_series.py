from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

from observability_client import DatadogMetricsClient
from observability_models import MetricComparisonResponse, MetricSeriesResponse, MetricWindowRequest


def compare_metric_series(metric_name: str, left_filter: Dict[str, str], right_filter: Dict[str, str], start_time: Optional[datetime] = None, end_time: Optional[datetime] = None) -> MetricComparisonResponse:
    end_time = end_time or datetime.now(timezone.utc)
    start_time = start_time or (end_time - timedelta(hours=12))
    client = DatadogMetricsClient()
    left = MetricSeriesResponse.from_api(
        metric_name,
        client.query_metric_window(MetricWindowRequest(metric_name=metric_name, start_time=start_time, end_time=end_time, resource_filter=left_filter)),
    )
    right = MetricSeriesResponse.from_api(
        metric_name,
        client.query_metric_window(MetricWindowRequest(metric_name=metric_name, start_time=start_time, end_time=end_time, resource_filter=right_filter)),
    )
    return MetricComparisonResponse(metric_name=metric_name, left=left, right=right)
