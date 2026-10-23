# Query Datadog metric data filtered by resource labels or dimensions (tags).

import os
from .observability_client import init_client
from .observability_models import request_metric_window, normalize_datadog_points

api = init_client(os.getenv("DD_API_KEY"), os.getenv("DD_APP_KEY"))

METRIC = "system.cpu.user"
DIMENSION_FILTER = "env:prod"
WINDOW = "last_15m"


def filter_metric_dimensions():
    """Filter metric data by tags and retrieve points for the time window."""
    payload = {
        "query": f"{METRIC}{{tag:{DIMENSION_FILTER}}}",
        **request_metric_window({"window": WINDOW}),
    }
    response = api.Metric.query(**payload)
    return normalize_datadog_points(response)


if __name__ == "__main__":
    filtered = filter_metric_dimensions()
    print(filtered)

# ---------------------------------------------------------------------------
# Example: filter by multiple tags
# ---------------------------------------------------------------------------
# payload['query'] = f'{METRIC}{{tag:{DIMENSION_FILTER}},tag:{"region:us-east-1"}}'  # noqa
