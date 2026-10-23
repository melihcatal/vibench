"""
Observability client helper for Datadog Metrics API integration.

Provides configuration loading, authenticated session management,
and utility functions for constructing Datadog API requests.
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

DATADOG_API_BASE = "https://api.datadoghq.com/api/v2"
DATADOG_QUERY_BASE = "https://api.datadoghq.com/api/v1/query"


def get_datadog_api_key() -> str:
    """Retrieve Datadog API key from environment."""
    api_key = os.environ.get("DD_API_KEY")
    if not api_key:
        raise EnvironmentError("DD_API_KEY environment variable is required")
    return api_key


def get_datadog_app_key() -> str:
    """Retrieve Datadog application key from environment."""
    app_key = os.environ.get("DD_APP_KEY")
    if not app_key:
        raise EnvironmentError("DD_APP_KEY environment variable is required")
    return app_key


def get_datadog_site() -> str:
    """Retrieve Datadog site domain from environment, defaulting to datadoghq.com."""
    return os.environ.get("DD_SITE", "datadoghq.com")


def create_datadog_session() -> requests.Session:
    """Create a configured requests session with Datadog authentication headers."""
    session = requests.Session()
    session.headers.update({
        "DD-API-KEY": get_datadog_api_key(),
        "DD-APPLICATION-KEY": get_datadog_app_key(),
        "Content-Type": "application/json",
        "Accept": "application/json",
    })
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def normalize_metric_name(metric_name: str) -> str:
    """Normalize a metric name for Datadog queries."""
    return metric_name.strip().lower().replace(" ", "_")


def build_time_window(
    minutes: int = 60,
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
) -> tuple[int, int]:
    """
    Build a time window tuple (from_ts, to_ts) in epoch seconds.

    Args:
        minutes: Window duration in minutes when start/end not provided.
        start: Optional explicit start datetime.
        end: Optional explicit end datetime.

    Returns:
        Tuple of (from_ts, to_ts) as epoch seconds.
    """
    if end is None:
        end = datetime.now(timezone.utc)
    if start is None:
        start = end - timedelta(minutes=minutes)
    return (int(start.timestamp()), int(end.timestamp()))


def build_datadog_query_url(site: Optional[str] = None) -> str:
    """Build the Datadog query endpoint URL."""
    site = site or get_datadog_site()
    return f"https://api.{site}/api/v1/query"


def build_datadog_v2_url(site: Optional[str] = None, endpoint: str = "") -> str:
    """Build a Datadog v2 API endpoint URL."""
    site = site or get_datadog_site()
    base = f"https://api.{site}/api/v2"
    if endpoint:
        return f"{base}/{endpoint.lstrip('/')}"
    return base
