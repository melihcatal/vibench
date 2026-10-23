import datetime
from google.cloud import monitoring_v3
from .observability_client import query_time_series
from .observability_models import MetricQuery, TimeInterval, MetricResponse

def query_metric_window(metric_name: str, duration_hours: int = 1) -> list[float]:
    end_time = datetime.datetime.utcnow()
    start_time = end_time - datetime.timedelta(hours=duration_hours)
    interval = TimeInterval(start_time=start_time, end_time=end_time)
    query = MetricQuery(metric_type=metric_name)
    response: MetricResponse = query_time_series(query, interval)
    return [point.value for point in response.points]