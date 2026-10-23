from datetime import datetime, timedelta, timezone
from observability_client import build_datadog_session, get_datadog_base_url
from observability_models import MetricQuery, normalize_datadog_series


def compare_metric_series(metric_name, left_filter, right_filter, start_time=None, end_time=None, window_minutes=60):
    end_time = end_time or datetime.now(timezone.utc)
    if start_time is None:
        start_time = end_time - timedelta(minutes=window_minutes)
    session = build_datadog_session()
    base = f"{get_datadog_base_url()}/api/v1/query"
    left_query = MetricQuery(metric_name=metric_name, start_time=start_time, end_time=end_time, tags=[left_filter])
    right_query = MetricQuery(metric_name=metric_name, start_time=start_time, end_time=end_time, tags=[right_filter])
    left = session.get(base, params={"from": int(start_time.timestamp()), "to": int(end_time.timestamp()), "query": left_query.to_datadog_query()}, timeout=30)
    right = session.get(base, params={"from": int(start_time.timestamp()), "to": int(end_time.timestamp()), "query": right_query.to_datadog_query()}, timeout=30)
    left.raise_for_status()
    right.raise_for_status()
    return {"left": normalize_datadog_series(left.json()), "right": normalize_datadog_series(right.json())}
