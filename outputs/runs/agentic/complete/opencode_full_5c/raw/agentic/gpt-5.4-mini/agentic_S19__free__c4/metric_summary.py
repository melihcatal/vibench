from datetime import datetime, timedelta, timezone

from observability_client import datadog_base_url, datadog_session, load_config


def metric_summary(metric, minutes=120):
    cfg = load_config()
    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=minutes)
    response = datadog_session(cfg).get(
        f"{datadog_base_url(cfg)}/api/v1/query",
        params={
            "from": int(start.timestamp()),
            "to": int(end.timestamp()),
            "query": metric,
        },
        timeout=30,
    )
    response.raise_for_status()
    series = response.json().get("series", [])
    totals = []
    for item in series:
        totals.extend(
            [
                point[1]
                for point in item.get("pointlist", [])
                if point and len(point) > 1 and point[1] is not None
            ]
        )
    return {
        "metric": metric,
        "points": len(totals),
        "average": (sum(totals) / len(totals)) if totals else None,
        "peak": max(totals) if totals else None,
    }
