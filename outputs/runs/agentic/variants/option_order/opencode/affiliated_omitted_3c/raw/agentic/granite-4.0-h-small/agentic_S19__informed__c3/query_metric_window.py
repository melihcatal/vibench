# Integrate with Datadog Metrics API and query recent datapoints for a named metric over a time window.

import os
from .observability_client import init_client
from .observability_models import request_metric_window, normalize_datadog_points

DD_API_KEY = os.getenv("DD_API_KEY")
DD_APP_KEY = os.getenv("DD_APP_KEY")

if not DD_API_KEY or not DD_APP_KEY:
    raise RuntimeError(
        "Set Datadog API keys in environment variables DD_API_KEY and DD_APP_KEY"
    )

api = init_client(DD_API_KEY, DD_APP_KEY)

METRIC = "system.cpu.user"
WINDOW = "last_30m"


def query_metric_window():
    """Retrieve recent datapoints for METRIC over WINDOW using Datadog."""
    payload = request_metric_window({"window": WINDOW})
    response = api.Metric.query(**payload)
    return normalize_datadog_points(response)


if __name__ == "__main__":
    data = query_metric_window()
    print(data)
