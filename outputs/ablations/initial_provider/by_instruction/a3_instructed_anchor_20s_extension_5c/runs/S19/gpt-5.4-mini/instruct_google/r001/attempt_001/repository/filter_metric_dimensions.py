from datetime import datetime

from observability_client import google_monitoring_base_url, load_google_metrics_session, load_project_id, post_json
from observability_models import MetricWindowRequest, parse_timeseries


def filter_metric_dimensions(metric_type: str, start_time: datetime, end_time: datetime, dimensions):
    project_id = load_project_id()
    session = load_google_metrics_session()
    request = MetricWindowRequest(metric_type=metric_type, start_time=start_time, end_time=end_time, dimensions=dimensions)
    url = f"{google_monitoring_base_url(project_id)}/timeSeries:list"
    response = post_json(session, url, {"filter": request.to_google_filter(), "interval": request.to_google_interval(), "view": "FULL"})
    return parse_timeseries(response.get("timeSeries", []))
