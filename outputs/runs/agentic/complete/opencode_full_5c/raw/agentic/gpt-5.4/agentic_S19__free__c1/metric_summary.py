from __future__ import annotations

from datetime import datetime
from typing import Dict, Optional

from aggregate_metric_stats import aggregate_metric_stats
from observability_client import GoogleCloudMonitoringClient
from observability_models import MetricSummary


def metric_summary(
    metric_type: str,
    start_time: datetime,
    end_time: datetime,
    resource_type: Optional[str] = None,
    resource_labels: Optional[Dict[str, str]] = None,
    metric_labels: Optional[Dict[str, str]] = None,
    client: Optional[GoogleCloudMonitoringClient] = None,
) -> MetricSummary:
    stats = aggregate_metric_stats(
        metric_type=metric_type,
        start_time=start_time,
        end_time=end_time,
        resource_type=resource_type,
        resource_labels=resource_labels,
        metric_labels=metric_labels,
        client=client,
    )
    trend = "stable"
    anomaly_detected = False
    if stats.latest is not None and stats.average is not None:
        if stats.latest > stats.average * 1.2:
            trend = "up"
        elif stats.latest < stats.average * 0.8:
            trend = "down"
        anomaly_detected = stats.maximum is not None and stats.latest >= stats.maximum
    summary_text = (
        f"Google Cloud Monitoring metric {metric_type} is {trend} over the observed window; "
        f"latest={stats.latest}, average={stats.average}, min={stats.minimum}, max={stats.maximum}."
    )
    return MetricSummary(
        metric_type=metric_type,
        window_start=start_time,
        window_end=end_time,
        average=stats.average,
        latest=stats.latest,
        trend=trend,
        anomaly_detected=anomaly_detected,
        summary_text=summary_text,
    )
