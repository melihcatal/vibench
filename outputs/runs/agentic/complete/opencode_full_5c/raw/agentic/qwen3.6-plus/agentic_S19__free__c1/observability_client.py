import os
from datetime import datetime, timedelta
from typing import Any, Optional

import requests
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v1.api.metrics_api import MetricsApi
from datadog_api_client.v1.model.metrics_query_request import (
    MetricsQueryRequest as DDQueryRequest,
)

from observability_models import (
    MetricAggregation,
    MetricQueryRequest,
    MetricQueryResponse,
    normalize_datadog_response,
    parse_datadog_error,
)


DATADOG_API_HOST = "api.datadoghq.com"
DATADOG_QUERY_ENDPOINT = "https://api.datadoghq.com/api/v1/query"


def load_datadog_config() -> Configuration:
    api_key = os.environ.get("DD_API_KEY")
    app_key = os.environ.get("DD_APP_KEY")
    if not api_key or not app_key:
        raise ValueError(
            "DD_API_KEY and DD_APP_KEY environment variables are required for Datadog integration"
        )
    config = Configuration()
    config.api_key["apiKeyAuth"] = api_key
    config.api_key["appKeyAuth"] = app_key
    config.host = DATADOG_API_HOST
    return config


def get_datadog_api_client() -> ApiClient:
    config = load_datadog_config()
    return ApiClient(config)


def get_metrics_api() -> MetricsApi:
    api_client = get_datadog_api_client()
    return MetricsApi(api_client)


def build_datadog_query_request(
    metric_name: str,
    start: datetime,
    end: datetime,
    aggregation: MetricAggregation = MetricAggregation.AVG,
    interval_seconds: int = 60,
    dimensions: Optional[dict[str, str]] = None,
) -> str:
    base = f"{aggregation.value}:{metric_name}"
    if dimensions:
        dim_parts = [f"{k}:{v}" for k, v in dimensions.items()]
        base = f"{base}{{{{{','.join(dim_parts)}}}}}"
    return base


def query_datadog_metrics(
    metric_name: str,
    start: datetime,
    end: datetime,
    aggregation: MetricAggregation = MetricAggregation.AVG,
    interval_seconds: int = 60,
    dimensions: Optional[dict[str, str]] = None,
) -> MetricQueryResponse:
    api_key = os.environ.get("DD_API_KEY")
    app_key = os.environ.get("DD_APP_KEY")
    query = build_datadog_query_request(
        metric_name, start, end, aggregation, interval_seconds, dimensions
    )
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
    }
    params = {
        "from": int(start.timestamp()),
        "to": int(end.timestamp()),
        "query": query,
    }
    if interval_seconds:
        params["interval"] = interval_seconds
    response = requests.get(
        DATADOG_QUERY_ENDPOINT, headers=headers, params=params, timeout=30
    )
    response.raise_for_status()
    raw_data = response.json()
    error = parse_datadog_error(raw_data)
    if error:
        return MetricQueryResponse(status="error", error=error)
    return normalize_datadog_response(raw_data)


def query_datadog_metrics_with_sdk(
    metric_name: str,
    start: datetime,
    end: datetime,
    aggregation: MetricAggregation = MetricAggregation.AVG,
    interval_seconds: int = 60,
    dimensions: Optional[dict[str, str]] = None,
) -> MetricQueryResponse:
    metrics_api = get_metrics_api()
    query = build_datadog_query_request(
        metric_name, start, end, aggregation, interval_seconds, dimensions
    )
    dd_request = DDQueryRequest(
        query=query,
        _from=int(start.timestamp()),
        to=int(end.timestamp()),
    )
    if interval_seconds:
        dd_request.interval = interval_seconds
    raw_response = metrics_api.query_metrics(body=dd_request)
    normalized = normalize_datadog_response(raw_response)
    return normalized


def validate_datadog_credentials() -> bool:
    api_key = os.environ.get("DD_API_KEY")
    app_key = os.environ.get("DD_APP_KEY")
    if not api_key or not app_key:
        return False
    headers = {
        "Accept": "application/json",
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
    }
    try:
        response = requests.get(
            "https://api.datadoghq.com/api/v1/validate",
            headers=headers,
            timeout=10,
        )
        return response.status_code == 200
    except requests.RequestException:
        return False
