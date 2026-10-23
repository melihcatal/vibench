from datetime import datetime

from observability_client import google_monitoring_base_url, load_google_metrics_session, load_project_id, post_json
from observability_models import MetricWindowRequest


def metric_summary(metric_type: str, start_time: datetime, end_time: datetime):
    project_id = load_project_id()
    session = load_google_metrics_session()
    request = MetricWindowRequest(metric_type=metric_type, start_time=start_time, end_time=end_time)
    url = f"{google_monitoring_base_url(project_id)}/timeSeries:list"
    payload = {"filter": request.to_google_filter(), "interval": request.to_google_interval(), "view": "FULL", "aggregation": {"alignmentPeriod": "300s", "perSeriesAligner": "ALIGN_RATE"}}
    return post_json(session, url, payload)
