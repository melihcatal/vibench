from datetime import datetime
from typing import Dict, Optional
import requests
from observability_client import get_metrics_config, build_headers, normalize_time_window
from observability_models import ComparisonRequest, ComparisonResponse, normalize_points, compare_point_lists

GOOGLE_MONITORING_API = "https://monitoring.googleapis.com"


def compare_metric_series(metric_name: str, resource_a: Dict[str, str], resource_b: Dict[str, str], start_time: Optional[datetime] = None, end_time: Optional[datetime] = None, window_minutes: int = 60, project_id: Optional[str] = None) -> ComparisonResponse:
    cfg = get_metrics_config()
    project = project_id or cfg.project_id
    if not project:
        raise ValueError("project_id is required for Google Cloud Monitoring")
    start_dt, end_dt = normalize_time_window(start_time, end_time, window_minutes)
    req = ComparisonRequest(metric_name=metric_name, resource_a=resource_a, resource_b=resource_b, start_time=start_dt, end_time=end_dt)
    url = f"{GOOGLE_MONITORING_API}/v3/projects/{project}/timeSeries"
    params_a = {
        "filter": req.to_filter(project, resource_a),
        "interval.startTime": req.start_time.isoformat().replace("+00:00", "Z"),
        "interval.endTime": req.end_time.isoformat().replace("+00:00", "Z"),
    }
    params_b = dict(params_a)
    params_b["filter"] = req.to_filter(project, resource_b)
    resp_a = requests.get(url, headers=build_headers(cfg), params=params_a, timeout=cfg.timeout_seconds)
    resp_b = requests.get(url, headers=build_headers(cfg), params=params_b, timeout=cfg.timeout_seconds)
    resp_a.raise_for_status()
    resp_b.raise_for_status()
    series_a = normalize_points(resp_a.json().get("timeSeries", []))
    series_b = normalize_points(resp_b.json().get("timeSeries", []))
    return ComparisonResponse(metric_name=metric_name, series_a=series_a, series_b=series_b, comparison=compare_point_lists(series_a, series_b), raw={"a": resp_a.json(), "b": resp_b.json()})
