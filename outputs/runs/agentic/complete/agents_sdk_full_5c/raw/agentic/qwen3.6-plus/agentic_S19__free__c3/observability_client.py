"""
observability_client.py
Local configuration and client helper utilities for Managed Metrics Monitoring.
Provides Datadog API client initialization, configuration loading, and shared utilities.
"""

import os
from typing import Optional, Dict, Any

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.metrics_api import MetricsApi
from datadog_api_client.v2.api.metrics_api import MetricsApi as MetricsApiV2


DATADOG_SITE_DEFAULT = "datadoghq.com"
DATADOG_API_BASE = "api.datadoghq.com"


def load_datadog_config(
    api_key: Optional[str] = None,
    app_key: Optional[str] = None,
    site: Optional[str] = None,
) -> Configuration:
    """Load Datadog API configuration from environment or explicit arguments."""
    api_key = api_key or os.environ.get("DATADOG_API_KEY", "")
    app_key = app_key or os.environ.get("DATADOG_APP_KEY", "")
    site = site or os.environ.get("DATADOG_SITE", DATADOG_SITE_DEFAULT)

    configuration = Configuration(
        api_key={
            "apiKeyAuth": api_key,
            "appKeyAuth": app_key,
        },
        host=f"https://{DATADOG_API_BASE}" if "datadog" not in site else f"https://api.{site}",
    )
    configuration.debug = os.environ.get("DATADOG_DEBUG", "0") == "1"
    return configuration


def get_metrics_api_v1(configuration: Optional[Configuration] = None) -> MetricsApi:
    """Return a Datadog Metrics API v1 client instance."""
    if configuration is None:
        configuration = load_datadog_config()
    api_client = ApiClient(configuration)
    return MetricsApi(api_client)


def get_metrics_api_v2(configuration: Optional[Configuration] = None) -> MetricsApiV2:
    """Return a Datadog Metrics API v2 client instance."""
    if configuration is None:
        configuration = load_datadog_config()
    api_client = ApiClient(configuration)
    return MetricsApiV2(api_client)


def build_datadog_headers(api_key: Optional[str] = None, app_key: Optional[str] = None) -> Dict[str, str]:
    """Build HTTP headers for direct Datadog REST API calls."""
    api_key = api_key or os.environ.get("DATADOG_API_KEY", "")
    app_key = app_key or os.environ.get("DATADOG_APP_KEY", "")
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
    }


def format_datadog_url(query_type: str, site: Optional[str] = None) -> str:
    """Format a Datadog API URL for direct HTTP requests."""
    site = site or os.environ.get("DATADOG_SITE", DATADOG_SITE_DEFAULT)
    base = f"https://api.{site}"
    endpoints = {
        "query": "/api/v1/query",
        "metrics": "/api/v2/query",
        "search": "/api/v2/search",
    }
    return base + endpoints.get(query_type, "/api/v1/query")


def extract_datadog_series(raw_response: Dict[str, Any]) -> list:
    """Extract series data from Datadog API responses."""
    if isinstance(raw_response, dict):
        series = raw_response.get("series", [])
        if not series and "data" in raw_response:
            series = raw_response["data"].get("attributes", {}).get("series", [])
        return series
    return []


def normalize_datadog_timestamp(ts: Any) -> float:
    """Normalize Datadog timestamps to epoch seconds."""
    try:
        return float(ts)
    except (ValueError, TypeError):
        return 0.0


def normalize_datadog_value(val: Any) -> Optional[float]:
    """Normalize metric values from Datadog responses."""
    if val is None:
        return None
    try:
        return float(val)
    except (ValueError, TypeError):
        return None
