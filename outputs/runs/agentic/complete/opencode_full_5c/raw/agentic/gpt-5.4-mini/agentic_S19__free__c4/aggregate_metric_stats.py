from datetime import datetime, timedelta, timezone

from observability_client import datadog_base_url, datadog_session, load_config


def aggregate_metric_stats(metric, minutes=60, scope=None):
    cfg = load_config()
    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=minutes)
    query = metric if not scope else f"{metric}{{{scope}}}"
    url = f"{datadog_base_url(cfg)}/api/v1/query"
    params = {
        "from": int(start.timestamp()),
        "to": int(end.timestamp()),
        "query": query,
    }
    payload = datadog_session(cfg).get(url, params=params, timeout=30)
    payload.raise_for_status()
    data = payload.json()
    stats = []
    for series in data.get("series", []):
        values = [
            point[1]
            for point in series.get("pointlist", [])
            if point and len(point) > 1 and point[1] is not None
        ]
        if values:
            stats.append(
                {
                    "scope": series.get("scope"),
                    "min": min(values),
                    "max": max(values),
                    "avg": sum(values) / len(values),
                }
            )
    return stats
