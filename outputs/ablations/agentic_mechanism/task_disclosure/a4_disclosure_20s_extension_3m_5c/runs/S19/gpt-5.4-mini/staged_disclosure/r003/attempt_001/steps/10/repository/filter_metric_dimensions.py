import os
from typing import Any, Dict, List, Optional

import requests


GENIUS_SPORTS_METRICS_API_BASE_URL = os.environ.get("GENIUS_SPORTS_METRICS_API_BASE_URL", "https://api.geniussports.com")
GENIUS_SPORTS_API_KEY = os.environ.get("GENIUS_SPORTS_API_KEY")


def filter_metric_dimensions(metric_name: str, dimensions: Optional[Dict[str, str]] = None, resource_labels: Optional[Dict[str, str]] = None, limit: int = 100) -> List[Dict[str, Any]]:
    if not GENIUS_SPORTS_API_KEY:
        raise ValueError("GENIUS_SPORTS_API_KEY is required")
    params: Dict[str, Any] = {"metric": metric_name, "limit": limit}
    if dimensions:
        for key, value in dimensions.items():
            params[f"dimension[{key}]"] = value
    if resource_labels:
        for key, value in resource_labels.items():
            params[f"resource_label[{key}]"] = value
    response = requests.get(
        f"{GENIUS_SPORTS_METRICS_API_BASE_URL}/v1/metrics/query",
        headers={"Authorization": f"Bearer {GENIUS_SPORTS_API_KEY}", "Accept": "application/json"},
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()
    if isinstance(payload, dict) and "data" in payload and isinstance(payload["data"], list):
        return payload["data"]
    if isinstance(payload, list):
        return payload
    return [payload]
