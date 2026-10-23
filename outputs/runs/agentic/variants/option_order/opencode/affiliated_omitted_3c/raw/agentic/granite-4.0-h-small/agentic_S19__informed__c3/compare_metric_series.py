# Compare metric values for two Datadog resources (hosts) over the same time window.

import os
from .observability_client import init_client
from .observability_models import normalize_datadog_points

api = init_client(os.getenv("DD_API_KEY"), os.getenv("DD_APP_KEY"))

METRIC = "system.cpu.user"
HOST_A = "host-01"
HOST_B = "host-02"
WINDOW = "last_10m"

METRIC_TAGS = {HOST_A: f"host:{HOST_A}", HOST_B: f"host:{HOST_B}"}


def compare_metric_series():
    """Retrieve and compare metric series for two hosts over a common window."""
    series = {}
    for name, tag in METRIC_TAGS.items():
        payload = {
            "query": f"{METRIC}{{tag:{tag}}}",
            **{
                k: v
                for k, v in request_metric_window({"window": WINDOW}).items()
                if k != "query"
            },
        }
        response = api.Metric.query(**payload)
        series[name] = normalize_datadog_points(response)
    return series


if __name__ == "__main__":
    compared = compare_metric_series()
    print(compared)

# ---------------------------------------------------------------------------
# Combine series into a unified view
# ---------------------------------------------------------------------------
# unified = {timestamp: {host: value}}
# for name, data in compared.items():
#     for point in data.get(METRIC, []):
#         ts = point['timestamp']
#         unified.setdefault(ts, {})[name] = point['value']
