"""
Observability client helper utilities for Managed Metrics Monitoring.

Provides configuration loading and client helper utilities shared across
metric query and aggregation integrations.
"""

import os
from typing import Optional, Dict, Any


def load_datadog_config() -> Dict[str, str]:
    """Load Datadog API configuration from environment variables.

    Returns:
        Dict with 'api_key', 'app_key', and 'site' for Datadog API access.
    """
    api_key = os.environ.get("DD_API_KEY")
    app_key = os.environ.get("DD_APP_KEY")
    site = os.environ.get("DD_SITE", "datadoghq.com")

    if not api_key or not app_key:
        raise ValueError(
            "DD_API_KEY and DD_APP_KEY environment variables are required "
            "for Datadog Metrics API access."
        )

    return {
        "api_key": api_key,
        "app_key": app_key,
        "site": site,
    }


def build_datadog_session(config: Optional[Dict[str, str]] = None) -> "requests.Session":
    """Build an authenticated requests session for the Datadog Metrics API.

    Args:
        config: Optional configuration dict. If not provided, loaded from env.

    Returns:
        Authenticated requests.Session configured for api.datadoghq.com.
    """
    import requests

    if config is None:
        config = load_datadog_config()

    session = requests.Session()
    session.headers.update({
        "DD-API-KEY": config["api_key"],
        "DD-APPLICATION-KEY": config["app_key"],
        "Content-Type": "application/json",
    })
    session.base_url = f"https://api.{config['site']}"
    return session


def normalize_timestamps(start_ts: int, end_ts: int) -> tuple[int, int]:
    """Validate and normalize epoch-second timestamps for metric queries.

    Args:
        start_ts: Start of the query window in epoch seconds.
        end_ts: End of the query window in epoch seconds.

    Returns:
        Tuple of (validated_start, validated_end) as integers.

    Raises:
        ValueError: If timestamps are invalid or start >= end.
    """
    import time

    now = int(time.time())

    if start_ts < 0:
        raise ValueError("start_ts must be a non-negative epoch timestamp")
    if end_ts < 0:
        raise ValueError("end_ts must be a non-negative epoch timestamp")
    if start_ts >= end_ts:
        raise ValueError("start_ts must be strictly less than end_ts")
    if end_ts > now + 3600:
        raise ValueError("end_ts cannot be more than 1 hour in the future")

    return start_ts, end_ts


def format_datadog_query(
    metric_name: str,
    rollup: str = "avg",
    aggregation: str = "avg",
    dimensions: Optional[Dict[str, str]] = None,
) -> str:
    """Format a Datadog metrics query string.

    Args:
        metric_name: The metric name, e.g., 'system.cpu.usage'.
        rollup: Rollup interval function (avg, sum, min, max).
        aggregation: Aggregation across matching series.
        dimensions: Optional tag filters like {'host': 'web-1'}.

    Returns:
        A Datadog query string like "avg:system.cpu.usage{host:web-1}.rollup(avg, 60)".
    """
    tag_parts = []
    if dimensions:
        for k, v in dimensions.items():
            tag_parts.append(f"{k}:{v}")
    tag_filter = ""
    if tag_parts:
        tag_filter = "{" + ",".join(tag_parts) + "}"

    return f"{rollup}:{metric_name}{tag_filter}.{rollup}(60)"
