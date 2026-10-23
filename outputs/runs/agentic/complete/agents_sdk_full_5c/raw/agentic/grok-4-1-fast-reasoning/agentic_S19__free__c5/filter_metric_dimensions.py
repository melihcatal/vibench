import datetime
from google.cloud import monitoring_v3
from .observability_client import query_time_series
from .observability_models import MetricQuery, TimeInterval

def filter_metric_dimensions(metric_name: str, dimension_filter: str, duration_hours: int = 1) -> list[float]:
    end_time = datetime.datetime.utcnow()
    start_time = end_time - datetime.timedelta(hours=duration_hours)
    interval = TimeInterval(start_time=start_time, end_time=end_time)
    full_filter = f'metric.type = "{metric_name}" AND ({dimension_filter})'
    query = MetricQuery(metric_type="", filter_str=full_filter)
    response = query_time_series(query, interval)
    return [point.value for point in response.points]