"""
Local configuration and client helper utilities for Managed Metrics Monitoring.
Uses Datadog API client as the concrete provider backend.
"""

import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.metrics_api import MetricsApi
from datadog_api_client.v1.api.metrics_query_api import MetricsQueryApi


def get_datadog_configuration() -> Configuration:
    """Create and return a Datadog API configuration from environment variables."""
    config = Configuration()
    config.api_key["apiKeyAuth"] = os.environ.get("DATADOG_API_KEY", "")
    config.api_key["appKeyAuth"] = os.environ.get("DATADOG_APP_KEY", "")
    config.host = os.environ.get("DATADOG_HOST", "https://api.datadoghq.com")
    return config


def get_metrics_api_client() -> MetricsApi:
    """Return a configured MetricsApi client for Datadog v1 API."""
    config = get_datadog_configuration()
    api_client = ApiClient(configuration=config)
    return MetricsApi(api_client)


def get_metrics_query_api_client() -> MetricsQueryApi:
    """Return a configured MetricsQueryApi client for Datadog metrics query endpoint."""
    config = get_datadog_configuration()
    api_client = ApiClient(configuration=config)
    return MetricsQueryApi(api_client)


def build_time_window(
    minutes_ago: Optional[int] = None,
    hours_ago: Optional[int] = None,
    start_ts: Optional[int] = None,
    end_ts: Optional[int] = None,
) -> tuple:
    """
    Build (from_ts, to_ts) tuple as Unix epoch seconds.
    If start_ts/end_ts are provided, use them directly.
    Otherwise compute from minutes_ago or hours_ago relative to now.
    """
    now = int(datetime.utcnow().timestamp())
    if start_ts is not None and end_ts is not None:
        return start_ts, end_ts
    if hours_ago is not None:
        start = now - (hours_ago * 3600)
        return start, now
    if minutes_ago is not None:
        start = now - (minutes_ago * 60)
        return start, now
    default_start = now - 3600
    return default_start, now


def normalize_datadog_metric_response(raw_response: Any) -> Dict[str, Any]:
    """
    Normalize a Datadog API response into a standard dict structure.
    Extracts series, group, and point data.
    """
    result = {"series": [], "metadata": {}}
    if hasattr(raw_response, "series"):
        for series_obj in raw_response.series:
            series_data = {
                "metric": getattr(series_obj, "metric", ""),
                "display_name": getattr(series_obj, "display_name", ""),
                "unit": getattr(series_obj, "unit", None),
                "scope": getattr(series_obj, "scope", ""),
                "aggr": getattr(series_obj, "aggr", ""),
                "pointlist": getattr(series_obj, "pointlist", []),
            }
            result["series"].append(series_data)
    if hasattr(raw_response, "query"):
        result["metadata"]["query"] = raw_response.query
    if hasattr(raw_response, "res_type"):
        result["metadata"]["res_type"] = raw_response.res_type
    if hasattr(raw_response, "message"):
        result["metadata"]["message"] = raw_response.message
    return result


def build_metric_query_string(
    metric_name: str,
    aggregation: Optional[str] = None,
    filter_tags: Optional[Dict[str, str]] = None,
    rollup_interval: Optional[int] = None,
) -> str:
    """
    Build a Datadog metric query string.
    Format: {agg}:{metric}{by_tag_filter}
    """
    agg = aggregation or "avg"
    query = f"{agg}:{metric_name}"
    if filter_tags:
        tag_parts = [f"{k}:{v}" for k, v in filter_tags.items()]
        query += "{" + ",".join(tag_parts) + "}"
    if rollup_interval:
        query += f".rollup({rollup_interval})"
    return query
