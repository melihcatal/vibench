from __future__ import annotations

import os
from datetime import timedelta
from typing import Dict, Optional

from google.cloud import monitoring_v3
from google.cloud.monitoring_v3.query import Query

from observability_models import MetricWindowRequest, to_rfc3339, utc_now


DEFAULT_MONITORING_HOST = "monitoring.googleapis.com"


def get_project_id(explicit_project_id: Optional[str] = None) -> str:
    project_id = explicit_project_id or os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")
    if not project_id:
        raise ValueError("A Google Cloud project id is required via argument or GOOGLE_CLOUD_PROJECT")
    return project_id


def monitoring_client() -> monitoring_v3.MetricServiceClient:
    return monitoring_v3.MetricServiceClient(client_options={"api_endpoint": DEFAULT_MONITORING_HOST})


def build_filter(metric_type: str, resource_type: Optional[str] = None, resource_labels: Optional[Dict[str, str]] = None, metric_labels: Optional[Dict[str, str]] = None) -> str:
    clauses = [f'metric.type = "{metric_type}"']
    if resource_type:
        clauses.append(f'resource.type = "{resource_type}"')
    for key, value in (resource_labels or {}).items():
        clauses.append(f'resource.labels.{key} = "{value}"')
    for key, value in (metric_labels or {}).items():
        clauses.append(f'metric.labels.{key} = "{value}"')
    return " AND ".join(clauses)


def time_interval_from_minutes(minutes: int) -> Dict[str, str]:
    end = utc_now()
    start = end - timedelta(minutes=minutes)
    return {"start_time": to_rfc3339(start), "end_time": to_rfc3339(end)}


def build_query(request: MetricWindowRequest) -> Query:
    project_id = get_project_id(request.project_id)
    interval = time_interval_from_minutes(request.minutes)
    return Query(
        monitoring_client(),
        project=project_id,
        metric_type=request.metric_type,
        end_time=utc_now(),
        minutes=request.minutes,
        filter_=build_filter(
            metric_type=request.metric_type,
            resource_type=request.resource_type,
            resource_labels=request.resource_labels,
            metric_labels=request.metric_labels,
        ),
    ).align(request.alignment_period_seconds, request.per_series_aligner)
