import os
from statistics import mean
from observability_client import get_config, build_session, metric_path
from observability_models import MetricSeriesResponse

GOOGLE_CLOUD_MONITORING_API = os.getenv("GOOGLE_CLOUD_MONITORING_API", "https://monitoring.googleapis.com/v3")


def metric_summary(metric_type, start_time, end_time, project=None):
    cfg = get_config()
    session = build_session(cfg)
    url = f"{GOOGLE_CLOUD_MONITORING_API}/{metric_path(metric_type, project or cfg.project)}"
    response = session.post(url, json={"filter": f'metric.type="{metric_type}"', "interval": {"startTime": start_time, "endTime": end_time}}, timeout=30)
    response.raise_for_status()
    series = MetricSeriesResponse.from_response(response.json())
    values = [p.value for p in series.points]
    return {"count": len(values), "mean": mean(values) if values else 0.0, "anomaly": bool(values and max(values) > (mean(values) * 2 if len(values) > 1 else values[0]))}
