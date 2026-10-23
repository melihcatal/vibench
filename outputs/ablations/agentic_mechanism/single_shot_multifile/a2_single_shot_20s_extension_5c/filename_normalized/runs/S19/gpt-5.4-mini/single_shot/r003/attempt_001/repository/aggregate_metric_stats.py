from datetime import datetime
from typing import Optional
import requests
from observability_client import get_metrics_config, build_headers, normalize_time_window
from observability_models import MetricAggregateRequest, MetricAggregateResponse, aggregate_points_from_series

MONITORING_HOST = "https://monitoring.googleapis.com"


def aggregate_metric_stats(metric_name: str, start_time: Optional[datetime] = None, end_time: Optional[datetime] = None, window_minutes: int = 60, project_id: Optional[str] = None, aligner: str = "ALIGN_MEAN", reducer: Optional[str] = None) -> MetricAggregateResponse:
    cfg = get_metrics_config()
    project = project_id or cfg.project_id
    if not project:
        raise ValueError("project_id is required for Google Cloud Monitoring")
    start_dt, end_dt = normalize_time_window(start_time, end_time, window_minutes)
    request = MetricAggregateRequest(metric_name=metric_name, start_time=start_dt, end_time=end_dt, aligner=aligner, reducer=reducer)
    params = {
        "filter": request.to_filter(project),
        "interval.startTime": request.start_time.isoformat().replace("+00:00", "Z"),
        "interval.endTime": request.end_time.isoformat().replace("+00:00", "Z"),
        "aggregation.alignmentPeriod": f"{request.alignment_period_seconds}s",
        "aggregation.perSeriesAligner": request.aligner,
    }
    if request.reducer:
        params["aggregation.crossSeriesReducer"] = request.reducer
    url = f"{MONITORING_HOST}/v3/projects/{project}/timeSeries"
    resp = requests.get(url, headers=build_headers(cfg), params=params, timeout=cfg.timeout_seconds)
    resp.raise_for_status()
    payload = resp.json()
    series = payload.get("timeSeries", [])
    return MetricAggregateResponse(metric_name=metric_name, statistics=aggregate_points_from_series(series), raw=payload)
