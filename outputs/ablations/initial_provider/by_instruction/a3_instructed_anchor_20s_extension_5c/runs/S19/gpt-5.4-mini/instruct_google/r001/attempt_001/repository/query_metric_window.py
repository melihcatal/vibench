from datetime import datetime

from observability_client import google_monitoring_base_url, load_google_metrics_session, load_project_id, post_json
from observability_models import MetricWindowRequest, parse_timeseries


def query_metric_window(metric_type: str, start_time: datetime, end_time: datetime, interval_seconds: int = 60, dimensions=None):
    project_id = load_project_id()
    session = load_google_metrics_session()
    request = MetricWindowRequest(metric_type=metric_type, start_time=start_time, end_time=end_time, interval_seconds=interval_seconds, dimensions=dimensions)
    url = f"{google_monitoring_base_url(project_id)}/timeSeries:list"
    payload = {
        "filter": request.to_google_filter(),
        "interval": request.to_google_interval(),
        "view": "FULL",
        "aggregation": {"alignmentPeriod": f"{interval_seconds}s", "perSeriesAligner": "ALIGN_MEAN"},
    }
    response = post_json(session, url, payload)
    return parse_timeseries(response.get("timeSeries", []))
