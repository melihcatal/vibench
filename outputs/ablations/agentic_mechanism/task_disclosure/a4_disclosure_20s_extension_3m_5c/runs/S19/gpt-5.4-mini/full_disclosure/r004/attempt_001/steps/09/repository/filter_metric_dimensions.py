import os
from typing import Any, Dict, List, Optional

import requests


PROMETHEUS_BASE_URL = os.getenv("PROMETHEUS_BASE_URL", "http://localhost:9090")


def _build_matchers(metric_name: str, filters: Optional[Dict[str, str]] = None) -> str:
    matchers = [f'__name__="{metric_name}"']
    if filters:
        for key, value in filters.items():
            matchers.append(f'{key}="{value}"')
    return "{" + ",".join(matchers) + "}"


def filter_metric_dimensions(metric_name: str, filters: Optional[Dict[str, str]] = None, limit: int = 100) -> List[Dict[str, Any]]:
    query = _build_matchers(metric_name, filters)
    url = f"{PROMETHEUS_BASE_URL.rstrip('/')}/api/v1/series"
    response = requests.get(url, params={"match[]": query, "limit": limit}, timeout=30)
    response.raise_for_status()
    payload = response.json()
    if payload.get("status") != "success":
        raise RuntimeError(payload.get("error", "Prometheus query failed"))
    return payload.get("data", [])
