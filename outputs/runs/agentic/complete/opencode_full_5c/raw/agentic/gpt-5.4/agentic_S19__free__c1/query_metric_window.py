from __future__ import annotations

from datetime import datetime
from typing import Dict, List, Optional

from observability_client import (
    GoogleCloudMonitoringClient,
    default_metric_window_request,
)
from observability_models import MetricSeries


def query_metric_window(
    metric_type: str,
    start_time: datetime,
    end_time: datetime,
    resource_type: Optional[str] = None,
    resource_labels: Optional[Dict[str, str]] = None,
    metric_labels: Optional[Dict[str, str]] = None,
    alignment_period_seconds: int = 300,
    per_series_aligner: str = "ALIGN_MEAN",
    client: Optional[GoogleCloudMonitoringClient] = None,
) -> List[MetricSeries]:
    monitoring_client = client or GoogleCloudMonitoringClient()
    request = default_metric_window_request(
        metric_type=metric_type,
        start_time=start_time,
        end_time=end_time,
        resource_type=resource_type,
        resource_labels=resource_labels,
        metric_labels=metric_labels,
        alignment_period_seconds=alignment_period_seconds,
        per_series_aligner=per_series_aligner,
    )
    return monitoring_client.list_time_series(request)
