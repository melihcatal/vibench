from datetime import datetime, timedelta, timezone
from observability_client import build_datadog_session, get_datadog_base_url
from observability_models import MetricQuery, normalize_datadog_series


def metric_summary(metric_name, window_minutes=120, tags=None):
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=window_minutes)
    query = MetricQuery(metric_name=metric_name, start_time=start_time, end_time=end_time, tags=tags or [])
    session = build_datadog_session()
    response = session.get(f"{get_datadog_base_url()}/api/v1/query", params={"from": int(start_time.timestamp()), "to": int(end_time.timestamp()), "query": query.to_datadog_query()}, timeout=30)
    response.raise_for_status()
    series = normalize_datadog_series(response.json())
    values = [v for item in series for v in item.get("values", [])]
    if not values:
        return {"metric": metric_name, "trend": "no_data", "anomalies": []}
    trend = "up" if values[-1] > values[0] else "down" if values[-1] < values[0] else "flat"
    anomalies = [v for v in values if v > max(values) * 0.95]
    return {"metric": metric_name, "trend": trend, "anomalies": anomalies, "points": len(values)}
