from datetime import datetime, timedelta, timezone
from typing import Any, Dict, Optional
import os
import requests
from observability_client import get_metrics_config, build_headers, normalize_time_window
from observability_models import MetricSeriesRequest, MetricSeriesResponse, normalize_points

ORCHESTRATOR_API_HOST = "https://monitoring.googleapis.com"


def query_metric_window(metric_name: str, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None, window_minutes: int = 60, project_id: Optional[str] = None, filter_expression: Optional[str] = None) -> MetricSeriesResponse:
    cfg = get_metrics_config()
    project = project_id or cfg.project_id
    if not project:
        raise ValueError("project_id is required for Google Cloud Monitoring")
    start_dt, end_dt = normalize_time_window(start_time, end_time, window_minutes)
    request = MetricSeriesRequest(metric_name=metric_name, start_time=start_dt, end_time=end_dt, filter_expression=filter_expression)
    params = {
        "filter": request.to_filter(project),
        "interval.startTime": request.start_time.isoformat().replace("+00:00", "Z"),
        "interval.endTime": request.end_time.isoformat().replace("+00:00", "Z"),
    }
    url = f"{ORCHESTRATOR_API_HOST}/v3/projects/{project}/timeSeries"
    resp = requests.get(url, headers=build_headers(cfg), params=params, timeout=cfg.timeout_seconds)
    resp.raise_for_status()
    payload = resp.json()
    return MetricSeriesResponse(metric_name=metric_name, points=normalize_points(payload.get("timeSeries", [])), raw=payload)
