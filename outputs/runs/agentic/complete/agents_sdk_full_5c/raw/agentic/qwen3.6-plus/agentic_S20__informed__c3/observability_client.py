"""
Local configuration and client helper utilities for Managed Log Query / Log Ingestion.
Configures Datadog Logs API access via DD_API_KEY and DD_APP_KEY.
"""

import os
from typing import Dict, Optional
import requests

DATADOG_LOGS_API_BASE = "https://api.datadoghq.com/api/v2"
DATADOG_INGESTION_BASE = "https://http-intake.logs.datadoghq.com"


def get_datadog_api_key() -> str:
    """Retrieve Datadog API key from environment."""
    api_key = os.environ.get("DD_API_KEY")
    if not api_key:
        raise ValueError("DD_API_KEY environment variable is required")
    return api_key


def get_datadog_app_key() -> str:
    """Retrieve Datadog application key from environment."""
    app_key = os.environ.get("DD_APP_KEY")
    if not app_key:
        raise ValueError("DD_APP_KEY environment variable is required")
    return app_key


def build_query_headers() -> Dict[str, str]:
    """Build standard headers for Datadog Logs query API calls."""
    return {
        "DD-API-KEY": get_datadog_api_key(),
        "DD-APPLICATION-KEY": get_datadog_app_key(),
        "Content-Type": "application/json",
    }


def build_ingestion_headers() -> Dict[str, str]:
    """Build standard headers for Datadog log ingestion API calls."""
    return {
        "DD-API-KEY": get_datadog_api_key(),
        "Content-Type": "application/json",
    }


def ingest_logs_to_datadog(log_events: list, tags: str = "") -> dict:
    """Send structured log events to Datadog Logs Ingestion API."""
    url = f"{DATADOG_INGESTION_BASE}/api/v2/logs"
    headers = build_ingestion_headers()
    payload = {
        "ddtags": tags,
        "logs": log_events,
    }
    response = requests.post(url, headers=headers, json=payload, timeout=30)
    response.raise_for_status()
    return response.json()


def query_datadog_logs(params: Dict[str, str]) -> dict:
    """Execute a logs query against the Datadog Logs API v2."""
    url = f"{DATADOG_LOGS_API_BASE}/logs/events/search"
    headers = build_query_headers()
    body = {
        "filter": {
            "query": params.get("filter[query]", ""),
            "from": params.get("filter[from]"),
            "to": params.get("filter[to]"),
            "limit": int(params.get("filter[limit]", 100)),
        },
        "sort": params.get("sort", "timestamp"),
    }
    response = requests.post(url, headers=headers, json=body, timeout=30)
    response.raise_for_status()
    return response.json()
