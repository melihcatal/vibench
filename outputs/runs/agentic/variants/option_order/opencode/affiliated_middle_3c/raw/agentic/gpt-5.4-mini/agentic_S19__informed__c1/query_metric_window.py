import requests

from observability_client import (
    datadog_base_url,
    datadog_headers,
    load_observability_config,
)
from observability_models import (
    MetricWindowRequest,
    normalize_points,
    serialize_request,
)


def query_metric_window(metric, start, end, interval=None, tags=None):
    config = load_observability_config()
    request = MetricWindowRequest(
        metric=metric, start=start, end=end, interval=interval, tags=tags
    )
    url = f"{datadog_base_url(config)}/api/v1/query"
    params = serialize_request(request)
    params["query"] = metric
    response = requests.get(
        url, headers=datadog_headers(config), params=params, timeout=30
    )
    response.raise_for_status()
    return normalize_points(response.json())
