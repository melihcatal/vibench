import datetime
from google.cloud import monitoring_v3
from .observability_client import query_time_series
from .observability_models import MetricQuery, TimeInterval, MetricResponse

def compare_metric_series(filter1: str, filter2: str, duration_hours: int = 1) -> tuple[list[float], list[float]]:
    end_time = datetime.datetime.utcnow()
    start_time = end_time - datetime.timedelta(hours=duration_hours)
    interval = TimeInterval(start_time=start_time, end_time=end_time)
    query1 = MetricQuery(metric_type="", filter_str=filter1)
    query2 = MetricQuery(metric_type="", filter_str=filter2)
    resp1: MetricResponse = query_time_series(query1, interval)
    resp2: MetricResponse = query_time_series(query2, interval)
    return (
        [point.value for point in resp1.points],
        [point.value for point in resp2.points]
    )