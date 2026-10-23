import os
from observability_client import get_config, build_session, metric_path
from observability_models import MetricWindowRequest, MetricSeriesResponse

GOOGLE_CLOUD_MONITORING_API = os.getenv("GOOGLE_CLOUD_MONITORING_API", "https://monitoring.googleapis.com/v3")


def filter_metric_dimensions(metric_type, start_time, end_time, labels=None, project=None):
    cfg = get_config()
    labels = labels or {}
    label_filters = [f'metric.label."{k}"="{v}"' for k, v in labels.items()]
    filter_expr = " AND ".join([f'metric.type="{metric_type}"'] + label_filters)
    req = MetricWindowRequest(metric_type=metric_type, start_time=start_time, end_time=end_time, filter_expr=filter_expr, project=project or cfg.project)
    session = build_session(cfg)
    url = f"{GOOGLE_CLOUD_MONITORING_API}/{metric_path(metric_type, req.project)}"
    response = session.post(url, json={"filter": req.to_params()["filter"], "interval": {"startTime": start_time, "endTime": end_time}}, timeout=30)
    response.raise_for_status()
    return MetricSeriesResponse.from_response(response.json())
