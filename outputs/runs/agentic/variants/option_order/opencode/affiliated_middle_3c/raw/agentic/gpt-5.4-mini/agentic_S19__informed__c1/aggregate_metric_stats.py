import requests

from observability_client import (
    datadog_base_url,
    datadog_headers,
    load_observability_config,
)


def aggregate_metric_stats(metric, start, end, aggr="avg", interval=60):
    config = load_observability_config()
    url = f"{datadog_base_url(config)}/api/v1/query"
    params = {
        "query": f"{aggr}:{metric}{{*}}",
        "from": start,
        "to": end,
        "interval": interval,
    }
    response = requests.get(
        url, headers=datadog_headers(config), params=params, timeout=30
    )
    response.raise_for_status()
    return response.json()
