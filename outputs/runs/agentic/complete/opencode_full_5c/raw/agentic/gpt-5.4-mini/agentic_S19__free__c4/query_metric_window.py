from datetime import datetime, timedelta, timezone

from observability_client import datadog_base_url, datadog_session, load_config
from observability_models import normalize_points


def query_metric_window(metric, minutes=60, scope=None):
    cfg = load_config()
    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=minutes)
    params = {
        "from": int(start.timestamp()),
        "to": int(end.timestamp()),
        "query": metric if not scope else f"{metric}{{{scope}}}",
    }
    response = datadog_session(cfg).get(
        f"{datadog_base_url(cfg)}/api/v1/query", params=params, timeout=30
    )
    response.raise_for_status()
    data = response.json()
    series = data.get("series", [])
    return [
        {
            "scope": item.get("scope"),
            "points": normalize_points(item.get("pointlist", [])),
        }
        for item in series
    ]
