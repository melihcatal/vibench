import requests

from observability_client import (
    datadog_base_url,
    datadog_headers,
    load_observability_config,
)


def compare_metric_series(metric, start, end, left_dimensions, right_dimensions):
    config = load_observability_config()
    base_url = f"{datadog_base_url(config)}/api/v1/query"
    left_query = ",".join(f"{k}:{v}" for k, v in left_dimensions.items())
    right_query = ",".join(f"{k}:{v}" for k, v in right_dimensions.items())
    left = requests.get(
        base_url,
        headers=datadog_headers(config),
        params={"query": f"{metric}{{{left_query}}}", "from": start, "to": end},
        timeout=30,
    )
    right = requests.get(
        base_url,
        headers=datadog_headers(config),
        params={"query": f"{metric}{{{right_query}}}", "from": start, "to": end},
        timeout=30,
    )
    left.raise_for_status()
    right.raise_for_status()
    return {"left": left.json(), "right": right.json()}
