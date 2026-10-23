import os
from observability_client import get_config, build_session, metric_path
from observability_models import MetricSeriesComparisonRequest, MetricSeriesResponse

GOOGLE_CLOUD_MONITORING_API = os.getenv("GOOGLE_CLOUD_MONITORING_API", "https://monitoring.googleapis.com/v3")


def compare_metric_series(metric_type, start_time, end_time, filter_a, filter_b, project=None):
    cfg = get_config()
    req = MetricSeriesComparisonRequest(metric_type=metric_type, start_time=start_time, end_time=end_time, filter_a=filter_a, filter_b=filter_b, project=project or cfg.project)
    session = build_session(cfg)
    url = f"{GOOGLE_CLOUD_MONITORING_API}/{metric_path(metric_type, req.project)}"
    body_a = {"filter": f'metric.type="{metric_type}" AND {filter_a}', "interval": {"startTime": start_time, "endTime": end_time}}
    body_b = {"filter": f'metric.type="{metric_type}" AND {filter_b}', "interval": {"startTime": start_time, "endTime": end_time}}
    resp_a = session.post(url, json=body_a, timeout=30)
    resp_b = session.post(url, json=body_b, timeout=30)
    resp_a.raise_for_status()
    resp_b.raise_for_status()
    series_a = MetricSeriesResponse.from_response(resp_a.json())
    series_b = MetricSeriesResponse.from_response(resp_b.json())
    return {"a": series_a.raw, "b": series_b.raw, "delta_count": len(series_a.points) - len(series_b.points)}
