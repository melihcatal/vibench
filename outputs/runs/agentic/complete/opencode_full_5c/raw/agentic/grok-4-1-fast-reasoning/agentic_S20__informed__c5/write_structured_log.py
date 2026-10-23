import os
import requests
from typing import Dict, Any
from observability_client import build_datadog_headers, DD_SITE
from observability_models import LogData


def write_structured_log() -> None:
    api_key = os.getenv("DD_API_KEY")
    app_key = os.getenv("DD_APP_KEY")
    headers = build_datadog_headers(api_key, app_key)
    url = f"https://api.{DD_SITE}/api/v2/logs/events"
    log: LogData = {
        "message": "Structured log event with user data",
        "status": "info",
        "service": "user-service",
        "env": "staging",
        "user_id": 12345,
        "correlation_id": None,
    }
    response = requests.post(url, headers=headers, json=log)
    response.raise_for_status()
