import json
import os
import sys
from typing import Any, Dict, List, Optional

import requests


GRAFANA_CLOUD_METRICS_API = "https://prometheus-prod-10-prod-us-central-0.grafana.net/api/prom"


def _build_query(metric: str, labels: Dict[str, str]) -> str:
    if not labels:
        return metric
    matchers = []
    for key, value in labels.items():
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        matchers.append(f'{key}="{escaped}"')
    return f'{metric}{{{",".join(matchers)}}}'


def query_metric_data(metric: str, labels: Optional[Dict[str, str]] = None, time: Optional[str] = None) -> Dict[str, Any]:
    labels = labels or {}
    base_url = os.environ.get("GRAFANA_CLOUD_PROMETHEUS_URL", GRAFANA_CLOUD_METRICS_API).rstrip("/")
    username = os.environ.get("GRAFANA_CLOUD_PROMETHEUS_USERNAME")
    api_key = os.environ.get("GRAFANA_CLOUD_API_KEY")
    if not username or not api_key:
        raise RuntimeError("Missing Grafana Cloud credentials: GRAFANA_CLOUD_PROMETHEUS_USERNAME and GRAFANA_CLOUD_API_KEY")

    query = _build_query(metric, labels)
    params = {"query": query}
    if time:
        params["time"] = time

    response = requests.get(
        f"{base_url}/api/v1/query",
        params=params,
        auth=(username, api_key),
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    if payload.get("status") != "success":
        raise RuntimeError(payload)
    return payload


def main(argv: List[str]) -> int:
    if len(argv) < 2:
        print(json.dumps({"error": "usage: filter_metric_dimensions.py METRIC [key=value ...]"}))
        return 1

    metric = argv[1]
    labels: Dict[str, str] = {}
    for item in argv[2:]:
        if "=" not in item:
            raise ValueError(f"Invalid label filter: {item}")
        key, value = item.split("=", 1)
        labels[key] = value

    print(json.dumps(query_metric_data(metric, labels), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
