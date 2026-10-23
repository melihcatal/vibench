import os
import requests
from typing import Dict, Any
from observability_client import build_datadog_headers, DD_SITE
from observability_models import LogData


def write_correlated_logs(correlation_id: str = "corr-12345") -> None:
    api_key = os.getenv("DD_API_KEY")
    app_key = os.getenv("DD_APP_KEY")
    headers = build_datadog_headers(api_key, app_key)
    url = f"https://api.{DD_SITE}/api/v2/logs/events"
    logs = [
        {
            "message": f"Request {correlation_id} started",
            "status": "info",
            "service": "api-gateway",
            "correlation_id": correlation_id,
        },
        {
            "message": f"Processing step for {correlation_id}",
            "status": "info",
            "service": "api-gateway",
            "correlation_id": correlation_id,
        },
        {
            "message": f"Completed {correlation_id} with error",
            "status": "error",
            "service": "api-gateway",
            "correlation_id": correlation_id,
        },
    ]
    for log in logs:
        response = requests.post(url, headers=headers, json=log)
        response.raise_for_status()
