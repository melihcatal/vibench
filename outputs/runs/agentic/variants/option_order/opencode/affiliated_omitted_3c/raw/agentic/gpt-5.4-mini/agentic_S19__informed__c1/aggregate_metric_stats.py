from datetime import datetime, timedelta, timezone
from observability_client import build_datadog_session, get_datadog_base_url
from observability_models import MetricQuery, aggregate_series_payload


def aggregate_metric_stats(metric_name, start_time=None, end_time=None, window_minutes=60, tags=None, rollup="avg"):
    end_time = end_time or datetime.now(timezone.utc)
    if start_time is None:
        start_time = end_time - timedelta(minutes=window_minutes)
    query = MetricQuery(metric_name=metric_name, start_time=start_time, end_time=end_time, tags=tags or [])
    session = build_datadog_session()
    url = f"{get_datadog_base_url()}/api/v1/query"
    params = {
        "from": int(query.start_time.timestamp()),
        "to": int(query.end_time.timestamp()),
        "query": query.to_datadog_query(rollup=rollup),
    }
    response = session.get(url, params=params, timeout=30)
    response.raise_for_status()
    return aggregate_series_payload(response.json())
