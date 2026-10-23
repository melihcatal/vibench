from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional

import google.auth
from google.auth.transport.requests import AuthorizedSession

from observability_models import MetricWindowRequest, ensure_utc, to_rfc3339


MONITORING_BASE_URL = "https://monitoring.googleapis.com/v3"
MONITORING_READ_SCOPE = "https://www.googleapis.com/auth/monitoring.read"


class GoogleCloudMonitoringClient:
    def __init__(self, project_id: Optional[str] = None) -> None:
        credentials, detected_project = google.auth.default(scopes=[MONITORING_READ_SCOPE])
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT") or detected_project
        if not self.project_id:
            raise ValueError("A Google Cloud project_id is required via argument or GOOGLE_CLOUD_PROJECT")
        self.session = AuthorizedSession(credentials)

    def build_time_interval(self, minutes: int) -> Dict[str, str]:
        end_time = ensure_utc(datetime.now(timezone.utc))
        start_time = end_time - timedelta(minutes=minutes)
        return {
            "startTime": to_rfc3339(start_time),
            "endTime": to_rfc3339(end_time),
        }

    def build_filter(self, metric_type: str, extra_filter: Optional[str] = None) -> str:
        base = f'metric.type = "{metric_type}"'
        if extra_filter:
            return f"{base} AND {extra_filter}"
        return base

    def list_time_series(self, request: MetricWindowRequest, view: str = "FULL") -> Dict[str, Any]:
        params = {
            "filter": self.build_filter(request.metric_type, request.filter_text),
            "interval.startTime": self.build_time_interval(request.minutes)["startTime"],
            "interval.endTime": self.build_time_interval(request.minutes)["endTime"],
            "view": view,
            "aggregation.alignmentPeriod": f"{request.alignment_period_seconds}s",
            "aggregation.perSeriesAligner": request.per_series_aligner,
        }
        url = f"{MONITORING_BASE_URL}/projects/{self.project_id}/timeSeries"
        response = self.session.get(url, params=params, timeout=30)
        response.raise_for_status()
        return response.json()


def monitoring_client(project_id: Optional[str] = None) -> GoogleCloudMonitoringClient:
    return GoogleCloudMonitoringClient(project_id=project_id)
