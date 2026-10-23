from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

from observability_client import DatadogMetricsClient
from observability_models import MetricSeriesResponse, MetricWindowRequest


def query_metric_window(metric_name: str, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None, resource_filter: Optional[Dict[str, str]] = None) -> MetricSeriesResponse:
    end_time = end_time or datetime.now(timezone.utc)
    start_time = start_time or (end_time - timedelta(hours=1))
    client = DatadogMetricsClient()
    result: Dict[str, Any] = client.query_metric_window(
        MetricWindowRequest(metric_name=metric_name, start_time=start_time, end_time=end_time, resource_filter=resource_filter)
    )
    return MetricSeriesResponse.from_api(metric_name, result)
