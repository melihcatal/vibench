"""
Local configuration and client helper utilities for Managed Log Query / Log Ingestion.

Provides Datadog API client setup, credential loading, and shared request helpers
for log ingestion and querying workflows.
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

from datadog_api_client import Configuration, ApiClient
from datadog_api_client.v2.api.logs_api import LogsApi


def load_datadog_config() -> Configuration:
    """
    Load Datadog API configuration from environment variables.

    Required environment variables:
        DD_API_KEY - Datadog API key
        DD_APP_KEY - Datadog application key (optional for some endpoints)
        DD_SITE    - Datadog site (e.g. datadoghq.com, datadoghq.eu)

    Returns a configured Configuration object for Datadog API client.
    """
    api_key = os.environ.get("DD_API_KEY", "")
    app_key = os.environ.get("DD_APP_KEY", "")
    site = os.environ.get("DD_SITE", "datadoghq.com")

    config = Configuration()
    config.api_key["apiKeyAuth"] = api_key
    config.api_key["appKeyAuth"] = app_key
    config.server_variables = {"site": site}
    return config


def get_datadog_logs_client() -> LogsApi:
    """
    Create and return a Datadog LogsApi v2 client instance.

    Uses environment variables for authentication.
    """
    config = load_datadog_config()
    api_client = ApiClient(configuration=config)
    return LogsApi(api_client)


def build_log_ingestion_payload(
    log_entries: List[Dict[str, Any]],
    ddsource: str = "python",
    ddtags: str = "env:production",
    service: str = "default-service",
    hostname: str = "localhost",
) -> List[Dict[str, Any]]:
    """
    Build a batch log payload for Datadog log ingestion.

    Wraps each log entry with Datadog-specific metadata fields required
    by the /api/v2/logs endpoint.
    """
    wrapped = []
    for entry in log_entries:
        wrapped_entry = {
            "ddsource": ddsource,
            "ddtags": ddtags,
            "hostname": hostname,
            "service": service,
        }
        wrapped_entry.update(entry)
        wrapped.append(wrapped_entry)
    return wrapped


def send_logs_to_datadog(
    log_entries: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Send log entries directly to the Datadog Logs Intake API v2.

    Returns the response status and any error details.
    """
    import requests

    api_key = os.environ.get("DD_API_KEY", "")
    site = os.environ.get("DD_SITE", "datadoghq.com")
    url = f"https://http-intake.logs.{site}/api/v2/logs"

    headers = {
        "DD-API-KEY": api_key,
        "Content-Type": "application/json",
    }
    payload = {"ddsource": "python", "ddtags": "env:production", "service": "app"}

    if isinstance(log_entries, list) and len(log_entries) == 1:
        payload.update(log_entries[0])
        body = [payload]
    elif isinstance(log_entries, list):
        for entry in log_entries:
            entry.update({"ddsource": "python", "ddtags": "env:production"})
        body = log_entries
    else:
        payload.update(log_entries)
        body = [payload]

    response = requests.post(url, json=body, headers=headers)
    return {
        "status_code": response.status_code,
        "ok": response.ok,
        "content": response.text,
    }


def execute_log_query(
    query: str,
    time_from: str,
    time_to: str,
    limit: int = 50,
    sort: str = "timestamp",
) -> Dict[str, Any]:
    """
    Execute a log search query against Datadog v2 Logs Search API.

    Returns the raw JSON response body for further parsing.
    """
    import requests

    api_key = os.environ.get("DD_API_KEY", "")
    app_key = os.environ.get("DD_APP_KEY", "")
    site = os.environ.get("DD_SITE", "datadoghq.com")
    url = f"https://api.{site}/api/v2/logs/events/search"

    headers = {
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
        "Content-Type": "application/json",
    }

    body = {
        "filter": {
            "query": query,
            "from": time_from,
            "to": time_to,
        },
        "sort": sort,
        "page": {
            "limit": limit,
        },
    }

    response = requests.post(url, json=body, headers=headers)
    response.raise_for_status()
    return response.json()
