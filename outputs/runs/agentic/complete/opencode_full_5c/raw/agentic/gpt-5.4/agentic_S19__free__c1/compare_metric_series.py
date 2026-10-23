from __future__ import annotations

from datetime import datetime
from typing import Dict, Optional

from observability_client import (
    GoogleCloudMonitoringClient,
    default_metric_window_request,
)
from observability_models import MetricComparison


def _latest_value(series_list) -> tuple[Optional[float], Optional[str]]:
    latest_ts = None
    latest_value = None
    unit = None
    for series in series_list:
        for point in series.points:
            if point.value is not None and (
                latest_ts is None or point.interval_end > latest_ts
            ):
                latest_ts = point.interval_end
                latest_value = point.value
                unit = point.unit
    return latest_value, unit


def compare_metric_series(
    metric_type: str,
    start_time: datetime,
    end_time: datetime,
    left_label: str,
    left_resource_labels: Optional[Dict[str, str]] = None,
    left_metric_labels: Optional[Dict[str, str]] = None,
    right_label: str = "right",
    right_resource_labels: Optional[Dict[str, str]] = None,
    right_metric_labels: Optional[Dict[str, str]] = None,
    resource_type: Optional[str] = None,
    alignment_period_seconds: int = 300,
    per_series_aligner: str = "ALIGN_MEAN",
    client: Optional[GoogleCloudMonitoringClient] = None,
) -> MetricComparison:
    monitoring_client = client or GoogleCloudMonitoringClient()
    left_request = default_metric_window_request(
        metric_type=metric_type,
        start_time=start_time,
        end_time=end_time,
        resource_type=resource_type,
        resource_labels=left_resource_labels,
        metric_labels=left_metric_labels,
        alignment_period_seconds=alignment_period_seconds,
        per_series_aligner=per_series_aligner,
    )
    right_request = default_metric_window_request(
        metric_type=metric_type,
        start_time=start_time,
        end_time=end_time,
        resource_type=resource_type,
        resource_labels=right_resource_labels,
        metric_labels=right_metric_labels,
        alignment_period_seconds=alignment_period_seconds,
        per_series_aligner=per_series_aligner,
    )
    left_series = monitoring_client.list_time_series(left_request)
    right_series = monitoring_client.list_time_series(right_request)
    left_latest, unit = _latest_value(left_series)
    right_latest, right_unit = _latest_value(right_series)
    resolved_unit = unit or right_unit
    absolute_delta = None
    percent_delta = None
    if left_latest is not None and right_latest is not None:
        absolute_delta = left_latest - right_latest
        if right_latest != 0:
            percent_delta = (absolute_delta / right_latest) * 100.0
    return MetricComparison(
        left_label=left_label,
        right_label=right_label,
        window_start=start_time,
        window_end=end_time,
        left_latest=left_latest,
        right_latest=right_latest,
        absolute_delta=absolute_delta,
        percent_delta=percent_delta,
        unit=resolved_unit,
    )
