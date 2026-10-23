from __future__ import annotations

import os
from datetime import datetime
from typing import Dict, Iterable, Optional

import google.auth
from google.auth.transport.requests import AuthorizedSession

from observability_models import MetricWindowRequest, to_rfc3339


MONITORING_API_BASE = "https://monitoring.googleapis.com/v3"
GOOGLE_CLOUD_SCOPE = ["https://www.googleapis.com/auth/cloud-platform"]


class GoogleCloudMonitoringClient:
    def __init__(self, project_id: Optional[str] = None) -> None:
        credentials, detected_project = google.auth.default(scopes=GOOGLE_CLOUD_SCOPE)
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT") or detected_project
        if not self.project_id:
            raise ValueError("A Google Cloud project ID is required via GOOGLE_CLOUD_PROJECT or ADC.")
        self.session = AuthorizedSession(credentials)

    def project_name(self, project_id: Optional[str] = None) -> str:
        return f"projects/{project_id or self.project_id}"

    def list_time_series(self, request: MetricWindowRequest, view: str = "FULL") -> Dict:
        params = {
            "filter": self.build_filter(
                request.metric_type,
                request.resource_type,
                request.resource_labels,
            ),
            "interval.startTime": to_rfc3339(request.start_time),
            "interval.endTime": to_rfc3339(request.end_time),
            "aggregation.alignmentPeriod": f"{request.alignment_period_seconds}s",
            "aggregation.perSeriesAligner": request.per_series_aligner,
            "view": view,
        }
        url = f"{MONITORING_API_BASE}/{self.project_name(request.project_id)}/timeSeries"
        response = self.session.get(url, params=params, timeout=60)
        response.raise_for_status()
        return response.json()

    def build_filter(
        self,
        metric_type: str,
        resource_type: Optional[str] = None,
        resource_labels: Optional[Dict[str, str]] = None,
        metric_labels: Optional[Dict[str, str]] = None,
    ) -> str:
        clauses = [f'metric.type = "{metric_type}"']
        if resource_type:
            clauses.append(f'resource.type = "{resource_type}"')
        for key, value in (resource_labels or {}).items():
            clauses.append(f'resource.labels.{key} = "{value}"')
        for key, value in (metric_labels or {}).items():
            clauses.append(f'metric.labels.{key} = "{value}"')
        return " AND ".join(clauses)


def parse_iso8601(timestamp: str) -> datetime:
    normalized = timestamp.replace("Z", "+00:00")
    return datetime.fromisoformat(normalized)


def merge_dimension_filters(*filters: Optional[Dict[str, str]]) -> Dict[str, str]:
    merged: Dict[str, str] = {}
    for item in filters:
        if item:
            merged.update(item)
    return merged


def ensure_iterable_labels(labels: Optional[Iterable[str]]) -> list[str]:
    return [label for label in (labels or []) if label]
