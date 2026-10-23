from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Dict, Iterable, List, Optional

from google.cloud import monitoring_v3
from google.cloud.monitoring_v3.query import Query

from observability_models import (
    MetricPoint,
    MetricWindowRequest,
    parse_rfc3339,
    to_rfc3339,
)


def get_monitoring_client() -> monitoring_v3.MetricServiceClient:
    return monitoring_v3.MetricServiceClient()


def project_name(project_id: str) -> str:
    return f"projects/{project_id}"


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def build_time_interval(minutes: int) -> tuple[datetime, datetime]:
    end_time = utc_now()
    start_time = end_time - timedelta(minutes=minutes)
    return start_time, end_time


def build_filter(
    metric_type: str,
    resource_type: Optional[str] = None,
    labels: Optional[Dict[str, str]] = None,
) -> str:
    parts = [f'metric.type = "{metric_type}"']
    if resource_type:
        parts.append(f'resource.type = "{resource_type}"')
    for key, value in (labels or {}).items():
        label_key = (
            key
            if key.startswith(("resource.labels.", "metric.labels."))
            else f"resource.labels.{key}"
        )
        parts.append(f'{label_key} = "{value}"')
    return " AND ".join(parts)


def _typed_point_value(
    point_value: monitoring_v3.types.TypedValue,
) -> tuple[float, str]:
    kind = point_value.WhichOneof("value")
    raw = getattr(point_value, kind)
    if kind == "bool_value":
        return (1.0 if raw else 0.0, kind)
    return float(raw), kind


def normalize_time_series(
    series_iterable: Iterable[monitoring_v3.TimeSeries],
) -> List[MetricPoint]:
    normalized: List[MetricPoint] = []
    for series in series_iterable:
        for point in series.points:
            value, value_type = _typed_point_value(point.value)
            normalized.append(
                MetricPoint(
                    metric_type=series.metric.type,
                    resource_type=series.resource.type,
                    resource_labels=dict(series.resource.labels),
                    metric_labels=dict(series.metric.labels),
                    interval_start=to_rfc3339(point.interval.start_time)
                    if point.interval.start_time
                    else None,
                    interval_end=to_rfc3339(point.interval.end_time),
                    value=value,
                    value_type=value_type,
                )
            )
    normalized.sort(key=lambda item: parse_rfc3339(item.interval_end))
    return normalized


def run_query(request: MetricWindowRequest) -> List[MetricPoint]:
    start_time, end_time = build_time_interval(request.minutes)
    query = Query(
        client=get_monitoring_client(),
        project=request.project_id,
        metric_type=request.metric_type,
        end_time=end_time,
        days=0,
        hours=0,
        minutes=request.minutes,
    )
    if request.resource_type:
        query = query.select_resources(resource_type=request.resource_type)
    if request.labels:
        query = query.select_metrics(
            **{
                k.replace("metric.labels.", ""): v
                for k, v in request.labels.items()
                if k.startswith("metric.labels.")
            }
        )
    if request.alignment_period_seconds:
        query = query.align(
            request.per_series_aligner, seconds=request.alignment_period_seconds
        )
    if request.cross_series_reducer:
        query = query.reduce(request.cross_series_reducer, request.group_by_fields)
    series = list(query)
    points = normalize_time_series(series)
    return [
        point for point in points if parse_rfc3339(point.interval_end) >= start_time
    ]


def exportable_snapshot(points: List[MetricPoint]) -> List[Dict[str, object]]:
    return [
        {
            "metric_type": point.metric_type,
            "resource_type": point.resource_type,
            "resource_labels": point.resource_labels,
            "metric_labels": point.metric_labels,
            "interval_start": point.interval_start,
            "interval_end": point.interval_end,
            "value": point.value,
            "value_type": point.value_type,
            "provider": "google-cloud-monitoring",
            "credentials_env": os.getenv("GOOGLE_APPLICATION_CREDENTIALS"),
        }
        for point in points
    ]
