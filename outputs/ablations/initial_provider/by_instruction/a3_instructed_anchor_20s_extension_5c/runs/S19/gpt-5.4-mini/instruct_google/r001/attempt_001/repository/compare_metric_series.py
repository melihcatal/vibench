from datetime import datetime

from observability_client import google_monitoring_base_url, load_google_metrics_session, load_project_id, post_json
from observability_models import MetricWindowRequest, parse_timeseries


def compare_metric_series(metric_type: str, start_time: datetime, end_time: datetime, left_dimensions, right_dimensions):
    project_id = load_project_id()
    session = load_google_metrics_session()
    base_url = f"{google_monitoring_base_url(project_id)}/timeSeries:list"
    left = MetricWindowRequest(metric_type=metric_type, start_time=start_time, end_time=end_time, dimensions=left_dimensions)
    right = MetricWindowRequest(metric_type=metric_type, start_time=start_time, end_time=end_time, dimensions=right_dimensions)
    left_response = post_json(session, base_url, {"filter": left.to_google_filter(), "interval": left.to_google_interval(), "view": "FULL"})
    right_response = post_json(session, base_url, {"filter": right.to_google_filter(), "interval": right.to_google_interval(), "view": "FULL"})
    return {"left": parse_timeseries(left_response.get("timeSeries", [])), "right": parse_timeseries(right_response.get("timeSeries", []))}
