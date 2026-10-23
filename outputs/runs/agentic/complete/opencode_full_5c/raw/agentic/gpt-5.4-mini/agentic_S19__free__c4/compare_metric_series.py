from datetime import datetime, timedelta, timezone

from observability_client import datadog_base_url, datadog_session, load_config


def compare_metric_series(metric, left_dimensions, right_dimensions, minutes=60):
    cfg = load_config()
    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=minutes)

    def fetch(dimensions):
        filters = ",".join([f"{k}:{v}" for k, v in dimensions.items()])
        query = f"{metric}{{{filters}}}" if filters else metric
        response = datadog_session(cfg).get(
            f"{datadog_base_url(cfg)}/api/v1/query",
            params={
                "from": int(start.timestamp()),
                "to": int(end.timestamp()),
                "query": query,
            },
            timeout=30,
        )
        response.raise_for_status()
        return response.json().get("series", [])

    return {"left": fetch(left_dimensions), "right": fetch(right_dimensions)}
