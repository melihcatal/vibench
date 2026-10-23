import os
from typing import Dict, Any

# Example: using Datadog Metrics API
DD_API_KEY = os.getenv("DD_API_KEY")
DD_APP_KEY = os.getenv("DD_APP_KEY")


def get_datadog_headers() -> Dict[str, str]:
    return {
        "DD-API-KEY": DD_API_KEY,
        "DD-APPLICATION-KEY": DD_APP_KEY,
    }


def build_request_payload(
    metric: str,
    window_seconds: int,
    filters: Dict[str, Any] = None,
) -> Dict[str, Any]:
    payload = {
        "query": f'{metric}\\.as_count()\\.over("{window_seconds}s")',
    }
    if filters:
        payload["filters"] = filters
    return payload
