import os
from statistics import mean
from observability_client import get_config, build_session, metric_path
from observability_models import MetricAggregateRequest, MetricSeriesResponse

GOOGLE_CLOUD_MONITORING_API = os.getenv("GOOGLE_CLOUD_MONITORING_API", "https://monitoring.googleapis.com/v3")


def aggregate_metric_stats(metric_type, start_time, end_time, filter_expr=None, aggregation="mean", project=None):
    cfg = get_config()
    req = MetricAggregateRequest(metric_type=metric_type, start_time=start_time, end_time=end_time, filter_expr=filter_expr, aggregation=aggregation, project=project or cfg.project)
    session = build_session(cfg)
    url = f"{GOOGLE_CLOUD_MONITORING_API}/{metric_path(metric_type, req.project)}"
    body = {"filter": req.to_params()["filter"], "interval": {"startTime": start_time, "endTime": end_time}}
    response = session.post(url, json=body, timeout=30)
    response.raise_for_status()
    series = MetricSeriesResponse.from_response(response.json())
    values = [p.value for p in series.points]
    stats = {"count": len(values), "mean": mean(values) if values else 0.0, "min": min(values) if values else 0.0, "max": max(values) if values else 0.0}
    return {"stats": stats, "raw": series.raw}
