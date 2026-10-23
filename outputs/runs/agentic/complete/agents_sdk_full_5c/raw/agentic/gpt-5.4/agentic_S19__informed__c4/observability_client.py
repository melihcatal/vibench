from __future__ import annotations

import os
from datetime import timedelta
from typing import Optional

from google.cloud import monitoring_v3
from google.cloud.monitoring_v3.query import Query

from observability_models import MetricWindowRequest, to_rfc3339, utc_now


GOOGLE_MONITORING_PROVIDER = "Google Cloud Monitoring"


def get_project_id(explicit_project_id: Optional[str] = None) -> str:
    project_id = explicit_project_id or os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCLOUD_PROJECT")
    if not project_id:
        raise ValueError("Google Cloud project id is required via project_id, GOOGLE_CLOUD_PROJECT, or GCLOUD_PROJECT")
    return project_id


def build_metric_filter(request: MetricWindowRequest) -> str:
    if request.filter_expression:
        return request.filter_expression
    clauses = [f'metric.type = "{request.metric_type}"']
    if request.resource_type:
        clauses.append(f'resource.type = "{request.resource_type}"')
    return " AND ".join(clauses)


def get_metric_client() -> monitoring_v3.MetricServiceClient:
    return monitoring_v3.MetricServiceClient()


def project_name(project_id: str) -> str:
    return f"projects/{project_id}"


def time_interval_for_minutes(minutes: int) -> monitoring_v3.TimeInterval:
    end = utc_now()
    start = end - timedelta(minutes=minutes)
    interval = monitoring_v3.TimeInterval()
    interval.end_time.FromDatetime(end)
    interval.start_time.FromDatetime(start)
    return interval


def build_aggregation(request: MetricWindowRequest) -> monitoring_v3.Aggregation:
    aggregation = monitoring_v3.Aggregation(
        alignment_period={"seconds": request.alignment_period_seconds},
        per_series_aligner=request.per_series_aligner,
    )
    if request.cross_series_reducer:
        aggregation.cross_series_reducer = request.cross_series_reducer
    if request.group_by_fields:
        aggregation.group_by_fields.extend(request.group_by_fields)
    return aggregation


def build_query(request: MetricWindowRequest) -> Query:
    client = get_metric_client()
    return Query(
        client,
        project=get_project_id(request.project_id),
        metric_type=request.metric_type,
        minutes=request.minutes,
        end_time=utc_now(),
    )


def default_window_metadata(minutes: int) -> dict:
    end = utc_now()
    start = end - timedelta(minutes=minutes)
    return {"start_time": to_rfc3339(start), "end_time": to_rfc3339(end), "provider": GOOGLE_MONITORING_PROVIDER}
