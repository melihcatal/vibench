from datetime import datetime, timedelta, timezone
from observability_client import build_datadog_session, get_datadog_base_url
from observability_models import MetricQuery, normalize_datadog_series


def filter_metric_dimensions(metric_name, dimensions=None, resource_label=None, start_time=None, end_time=None, window_minutes=60):
    end_time = end_time or datetime.now(timezone.utc)
    if start_time is None:
        start_time = end_time - timedelta(minutes=window_minutes)
    tags = []
    if dimensions:
        tags.extend(f"{k}:{v}" for k, v in dimensions.items())
    if resource_label:
        tags.append(resource_label)
    query = MetricQuery(metric_name=metric_name, start_time=start_time, end_time=end_time, tags=tags)
    session = build_datadog_session()
    response = session.get(f"{get_datadog_base_url()}/api/v1/query", params={
        "from": int(query.start_time.timestamp()),
        "to": int(query.end_time.timestamp()),
        "query": query.to_datadog_query(),
    }, timeout=30)
    response.raise_for_status()
    return normalize_datadog_series(response.json())
