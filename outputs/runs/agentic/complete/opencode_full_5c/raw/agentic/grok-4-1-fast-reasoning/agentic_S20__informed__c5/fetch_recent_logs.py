import os
import requests
from typing import List, Dict, Any
from observability_client import build_datadog_headers, DD_SITE, time_range_ms
from observability_models import DatadogLogEntry


def fetch_recent_logs(
    service: str, min_duration: float, hours_back: int = 1
) -> List[DatadogLogEntry]:
    api_key = os.getenv("DD_API_KEY")
    app_key = os.getenv("DD_APP_KEY")
    headers = build_datadog_headers(api_key, app_key)
    start_ms, end_ms = time_range_ms(hours_back)
    query = f"service:{service} duration>{min_duration}"
    url = f"https://api.{DD_SITE}/api/v2/logs/events/search"
    body = {"query": query, "from": start_ms, "to": end_ms, "page": {"limit": 50}}
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    data = response.json()
    return data["data"]
