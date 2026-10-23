# Retrieve aggregated statistics for a metric over a time window using Datadog.

import os
from .observability_client import init_client
from .observability_models import normalize_datadog_points

api = init_client(os.getenv("DD_API_KEY"), os.getenv("DD_APP_KEY"))

METRIC = "system.cpu.user"
WINDOW = "last_5m"

METRIC_STATS = {
    "avg": "avg:{0}",
    "max": "max:{0}",
    "min": "min:{0}",
    "sum": "sum:{0}",
}


def aggregate_metric_stats() -> dict:
    """Fetch aggregated statistics for METRIC over WINDOW using Datadog."""
    payload = {
        "query": f"{METRIC_STATS['avg']}{{host:my-host}}",
        "start": int(
            (
                datetime.utcnow() - timedelta(minutes=int(WINDOW.split("_")[-1]))
            ).timestamp()
        ),
        "end": int(datetime.utcnow().timestamp()),
        "type": "avg",
    }
    response = api.Metric.query(**payload)
    return normalize_datadog_points(response)


if __name__ == "__main__":
    stats = aggregate_metric_stats()
    print(stats)
