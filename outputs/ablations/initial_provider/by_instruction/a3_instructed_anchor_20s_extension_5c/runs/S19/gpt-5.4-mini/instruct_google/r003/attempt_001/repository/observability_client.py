import os
from datetime import datetime
from typing import Any, Dict, List, Optional

import requests

from observability_models import MetricSeriesPoint, MetricSeriesResponse, normalize_dimensions, parse_iso_datetime


class GoogleCloudMonitoringClient:
    def __init__(self, project_id: Optional[str] = None, session: Optional[requests.Session] = None):
        self.project_id = project_id or os.getenv("GOOGLE_CLOUD_PROJECT") or os.getenv("GCP_PROJECT")
        self.session = session or requests.Session()
        self.base_url = "https://monitoring.googleapis.com/v3"
        self.token = os.getenv("GOOGLE_OAUTH_ACCESS_TOKEN")

    def _headers(self) -> Dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        response = self.session.get(f"{self.base_url}{path}", headers=self._headers(), params=params, timeout=60)
        response.raise_for_status()
        return response.json()

    def list_time_series(self, metric_type: str, start_time: datetime, end_time: datetime, filter_expr: Optional[str] = None) -> MetricSeriesResponse:
        if not self.project_id:
            raise ValueError("Missing Google Cloud project id")
        body_filter = [f'metric.type = "{metric_type}"']
        if filter_expr:
            body_filter.append(f"({filter_expr})")
        params = {
            "filter": " AND ".join(body_filter),
            "interval.startTime": start_time.isoformat().replace("+00:00", "Z"),
            "interval.endTime": end_time.isoformat().replace("+00:00", "Z"),
            "view": "FULL",
        }
        data = self._get(f"projects/{self.project_id}/timeSeries", params=params)
        points: List[MetricSeriesPoint] = []
        for series in data.get("timeSeries", []):
            dims = normalize_dimensions(series.get("metric", {}).get("labels"))
            for p in series.get("points", []):
                interval = p.get("interval", {})
                ts = interval.get("endTime") or interval.get("startTime")
                points.append(MetricSeriesPoint(timestamp=parse_iso_datetime(ts), value=float(p.get("value", {}).get("doubleValue", p.get("value", {}).get("int64Value", 0))), dimensions=dims))
        points.sort(key=lambda x: x.timestamp)
        return MetricSeriesResponse(metric_name=metric_type, points=points)
