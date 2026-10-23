from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

from observability_client import DatadogMetricsClient
from observability_models import MetricSeriesResponse, MetricWindowRequest


def filter_metric_dimensions(metric_name: str, dimensions: Dict[str, str], start_time: Optional[datetime] = None, end_time: Optional[datetime] = None) -> MetricSeriesResponse:
    end_time = end_time or datetime.now(timezone.utc)
    start_time = start_time or (end_time - timedelta(hours=6))
    client = DatadogMetricsClient()
    payload = client.filter_metric_dimensions(
        MetricWindowRequest(metric_name=metric_name, start_time=start_time, end_time=end_time, resource_filter=dimensions)
    )
    return MetricSeriesResponse.from_api(metric_name, payload)
