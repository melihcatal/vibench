import os
from typing import Any, Dict, Optional

import requests


API_BASE_URL = os.getenv("GENERIC_OBSERVABILITY_API_BASE_URL", "https://api.datadoghq.com")
API_KEY = os.getenv("DD_API_KEY")
APP_KEY = os.getenv("DD_APP_KEY")


def filter_metric_dimensions(
    metric_name: str,
    from_ts: int,
    to_ts: int,
    filter_query: Optional[str] = None,
    aggregation: str = "avg",
    interval: int = 60,
) -> Dict[str, Any]:
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
    }
    if API_KEY:
        headers["DD-API-KEY"] = API_KEY
    if APP_KEY:
        headers["DD-APPLICATION-KEY"] = APP_KEY

    params = {
        "from": from_ts,
        "to": to_ts,
        "query": f"{aggregation}:{metric_name}{{{filter_query or '*'}}}",
        "interval": interval,
    }

    response = requests.get(
        f"{API_BASE_URL.rstrip('/')}/api/v1/query",
        headers=headers,
        params=params,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


__all__ = ["filter_metric_dimensions"]
