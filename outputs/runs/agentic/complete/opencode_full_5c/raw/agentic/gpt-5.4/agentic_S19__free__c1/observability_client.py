from __future__ import annotations

import os
from datetime import datetime
from typing import Dict, Optional

import requests

from observability_models import (
    MetricWindowRequest,
    isoformat_utc,
    normalize_time_series,
)


class GoogleCloudMonitoringClient:
    def __init__(
        self,
        project_id: Optional[str] = None,
        access_token: Optional[str] = None,
        session: Optional[requests.Session] = None,
    ) -> None:
        self.project_id = (
            project_id
            or os.environ.get("GOOGLE_CLOUD_PROJECT")
            or os.environ.get("GCP_PROJECT")
        )
        self.access_token = access_token or os.environ.get("GCP_ACCESS_TOKEN")
        if not self.project_id:
            raise ValueError("Missing GOOGLE_CLOUD_PROJECT or GCP_PROJECT")
        if not self.access_token:
            raise ValueError("Missing GCP_ACCESS_TOKEN")
        self.session = session or requests.Session()
        self.base_url = "https://monitoring.googleapis.com/v3"

    def _headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json",
        }

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

    def list_time_series(
        self, request: MetricWindowRequest, page_size: int = 100
    ) -> list:
        params = {
            "filter": self.build_filter(
                metric_type=request.metric_type,
                resource_type=request.resource_type,
                resource_labels=request.resource_labels,
                metric_labels=request.metric_labels,
            ),
            "interval.startTime": isoformat_utc(request.start_time),
            "interval.endTime": isoformat_utc(request.end_time),
            "view": "FULL",
            "aggregation.alignmentPeriod": f"{request.alignment_period_seconds}s",
            "aggregation.perSeriesAligner": request.per_series_aligner,
            "pageSize": str(page_size),
        }
        if request.cross_series_reducer:
            params["aggregation.crossSeriesReducer"] = request.cross_series_reducer
        if request.group_by_fields:
            params["aggregation.groupByFields"] = request.group_by_fields
        url = f"{self.base_url}/projects/{self.project_id}/timeSeries"
        series = []
        page_token = None
        while True:
            page_params = dict(params)
            if page_token:
                page_params["pageToken"] = page_token
            response = self.session.get(
                url, headers=self._headers(), params=page_params, timeout=30
            )
            response.raise_for_status()
            payload = response.json()
            series.extend(
                normalize_time_series(item) for item in payload.get("timeSeries", [])
            )
            page_token = payload.get("nextPageToken")
            if not page_token:
                break
        return series


def default_metric_window_request(
    metric_type: str,
    start_time: datetime,
    end_time: datetime,
    resource_type: Optional[str] = None,
    resource_labels: Optional[Dict[str, str]] = None,
    metric_labels: Optional[Dict[str, str]] = None,
    alignment_period_seconds: int = 300,
    per_series_aligner: str = "ALIGN_MEAN",
) -> MetricWindowRequest:
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT")
    if not project_id:
        raise ValueError("Missing GOOGLE_CLOUD_PROJECT or GCP_PROJECT")
    return MetricWindowRequest(
        project_id=project_id,
        metric_type=metric_type,
        start_time=start_time,
        end_time=end_time,
        alignment_period_seconds=alignment_period_seconds,
        per_series_aligner=per_series_aligner,
        resource_type=resource_type,
        resource_labels=resource_labels or {},
        metric_labels=metric_labels or {},
    )
