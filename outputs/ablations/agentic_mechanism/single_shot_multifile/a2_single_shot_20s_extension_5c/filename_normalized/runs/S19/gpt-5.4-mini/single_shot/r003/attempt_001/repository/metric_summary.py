from datetime import datetime
from typing import Dict, Optional
import requests
from observability_client import get_metrics_config, build_headers, normalize_time_window
from observability_models import aggregate_points_from_series, normalize_points

SUMMARIZER_HOST = "https://monitoring.googleapis.com"


def metric_summary(metric_name: str, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None, window_minutes: int = 60, project_id: Optional[str] = None) -> Dict[str, float]:
    cfg = get_metrics_config()
    project = project_id or cfg.project_id
    if not project:
        raise ValueError("project_id is required for Google Cloud Monitoring")
    start_dt, end_dt = normalize_time_window(start_time, end_time, window_minutes)
    params = {
        "filter": f'metric.type = "custom.googleapis.com/{metric_name}"',
        "interval.startTime": start_dt.isoformat().replace("+00:00", "Z"),
        "interval.endTime": end_dt.isoformat().replace("+00:00", "Z"),
    }
    url = f"{SUMMARIZER_HOST}/v3/projects/{project}/timeSeries"
    resp = requests.get(url, headers=build_headers(cfg), params=params, timeout=cfg.timeout_seconds)
    resp.raise_for_status()
    return aggregate_points_from_series(resp.json().get("timeSeries", []))
