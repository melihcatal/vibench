from datetime import datetime
from typing import Dict, Optional
import requests
from observability_client import get_metrics_config, build_headers, normalize_time_window
from observability_models import DimensionFilterRequest, MetricSeriesResponse, normalize_points

GCLOUD_MONITORING_HOST = "https://monitoring.googleapis.com"


def filter_metric_dimensions(metric_name: str, dimensions: Optional[Dict[str, str]] = None, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None, window_minutes: int = 60, project_id: Optional[str] = None) -> MetricSeriesResponse:
    cfg = get_metrics_config()
    project = project_id or cfg.project_id
    if not project:
        raise ValueError("project_id is required for Google Cloud Monitoring")
    start_dt, end_dt = normalize_time_window(start_time, end_time, window_minutes)
    request = DimensionFilterRequest(metric_name=metric_name, dimensions=dimensions or {}, start_time=start_dt, end_time=end_dt)
    params = {
        "filter": request.to_filter(project),
        "interval.startTime": request.start_time.isoformat().replace("+00:00", "Z"),
        "interval.endTime": request.end_time.isoformat().replace("+00:00", "Z"),
    }
    url = f"{GCLOUD_MONITORING_HOST}/v3/projects/{project}/timeSeries"
    resp = requests.get(url, headers=build_headers(cfg), params=params, timeout=cfg.timeout_seconds)
    resp.raise_for_status()
    payload = resp.json()
    return MetricSeriesResponse(metric_name=metric_name, points=normalize_points(payload.get("timeSeries", [])), raw=payload)
