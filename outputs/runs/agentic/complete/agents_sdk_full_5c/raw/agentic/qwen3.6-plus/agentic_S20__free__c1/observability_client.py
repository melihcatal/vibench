"""
Local configuration and client helper utilities for Datadog Managed Log Query / Log Ingestion.

Provides authenticated Datadog API client construction, configuration loading,
and common retry / timeout settings for log write and query operations.
"""

import os
from datetime import datetime, timezone
from typing import Optional, Dict, Any

from datadog_api_client import Configuration, ApiClient
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.api.logs_aggregation_api import LogsAggregationApi


DATADOG_API_HOST = os.environ.get("DATADOG_API_HOST", "https://api.datadoghq.com")
DATADOG_API_KEY = os.environ.get("DATADOG_API_KEY", "")
DATADOG_APP_KEY = os.environ.get("DATADOG_APP_KEY", "")
DATADOG_SITE = os.environ.get("DATADOG_SITE", "datadoghq.com")
DEFAULT_TIMEOUT = 30
DEFAULT_PAGE_LIMIT = 100


def load_datadog_config() -> Configuration:
    """Load and return a Datadog API Configuration object from environment variables."""
    config = Configuration()
    config.api_key["apiKeyAuth"] = DATADOG_API_KEY
    config.api_key["appKeyAuth"] = DATADOG_APP_KEY
    config.host = DATADOG_API_HOST
    config.server_variables = {"site": DATADOG_SITE}
    config.retry = True
    config.server_index = 0
    return config


def get_logs_client() -> LogsApi:
    """Create and return an authenticated Datadog Logs API v2 client."""
    config = load_datadog_config()
    api_client = ApiClient(configuration=config)
    api_client.configuration.timeout = DEFAULT_TIMEOUT
    return LogsApi(api_client)


def get_logs_aggregation_client() -> LogsAggregationApi:
    """Create and return an authenticated Datadog Logs Aggregation API v2 client."""
    config = load_datadog_config()
    api_client = ApiClient(configuration=config)
    api_client.configuration.timeout = DEFAULT_TIMEOUT
    return LogsAggregationApi(api_client)


def build_datadog_log_payload(
    message: str,
    service: str = "default-service",
    env: str = "production",
    status: str = "info",
    ddsource: str = "python",
    attributes: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Build a Datadog-compatible log event payload with standard attributes."""
    timestamp = datetime.now(timezone.utc).isoformat()
    payload: Dict[str, Any] = {
        "message": message,
        "ddsource": ddsource,
        "service": service,
        "env": env,
        "status": status,
        "timestamp": timestamp,
        "hostname": os.environ.get("HOSTNAME", "unknown"),
    }
    if attributes:
        payload["attributes"] = attributes
    return payload


def build_correlation_attributes(
    correlation_id: str,
    trace_id: Optional[str] = None,
    span_id: Optional[str] = None,
    request_path: Optional[str] = None,
) -> Dict[str, Any]:
    """Build Datadog log attributes that include correlation identifiers."""
    attrs = {
        "correlation_id": correlation_id,
    }
    if trace_id:
        attrs["dd.trace_id"] = trace_id
    if span_id:
        attrs["dd.span_id"] = span_id
    if request_path:
        attrs["http.url"] = request_path
    return attrs


def format_datadog_timestamp(from_iso: str) -> str:
    """Convert an ISO timestamp to Datadog epoch-millisecond format."""
    dt = datetime.fromisoformat(from_iso.replace("Z", "+00:00"))
    return str(int(dt.timestamp() * 1000))
