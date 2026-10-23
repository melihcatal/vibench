import json
import os
from typing import Any, Dict, List, Optional

import requests


PROMETHEUS_API_BASE = os.getenv("PROMETHEUS_API_BASE", "https://prometheus.example.com")
PROMETHEUS_BEARER_TOKEN = os.getenv("PROMETHEUS_BEARER_TOKEN")


def _build_matchers(resource_labels: Optional[Dict[str, str]], dimensions: Optional[Dict[str, str]]) -> str:
    matchers: List[str] = []
    for source in (resource_labels or {}, dimensions or {}):
        for key, value in source.items():
            matchers.append(f'{key}="{value}"')
    return "{" + ",".join(matchers) + "}" if matchers else ""


def query_metric_data(metric_name: str, resource_labels: Optional[Dict[str, str]] = None, dimensions: Optional[Dict[str, str]] = None) -> Dict[str, Any]:
    query = f"{metric_name}{_build_matchers(resource_labels, dimensions)}"
    url = f"{PROMETHEUS_API_BASE.rstrip('/')}/api/v1/query"
    headers = {"Accept": "application/json"}
    if PROMETHEUS_BEARER_TOKEN:
        headers["Authorization"] = f"Bearer {PROMETHEUS_BEARER_TOKEN}"
    response = requests.get(url, params={"query": query}, headers=headers, timeout=30)
    response.raise_for_status()
    payload = response.json()
    if payload.get("status") != "success":
        raise RuntimeError(payload)
    return payload


def main() -> None:
    metric_name = os.getenv("METRIC_NAME", "up")
    resource_labels = json.loads(os.getenv("RESOURCE_LABELS", "{}"))
    dimensions = json.loads(os.getenv("DIMENSIONS", "{}"))
    result = query_metric_data(metric_name, resource_labels, dimensions)
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
