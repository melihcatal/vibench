import requests

from observability_client import (
    datadog_base_url,
    datadog_headers,
    load_observability_config,
)


def filter_metric_dimensions(metric, start, end, dimensions):
    config = load_observability_config()
    dimension_query = ",".join(f"{k}:{v}" for k, v in dimensions.items())
    url = f"{datadog_base_url(config)}/api/v1/query"
    params = {"query": f"{metric}{{{dimension_query}}}", "from": start, "to": end}
    response = requests.get(
        url, headers=datadog_headers(config), params=params, timeout=30
    )
    response.raise_for_status()
    return response.json()
