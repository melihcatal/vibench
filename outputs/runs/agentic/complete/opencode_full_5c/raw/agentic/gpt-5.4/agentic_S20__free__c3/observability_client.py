from __future__ import annotations

import os
from typing import Any, Dict, Iterable, List, Optional

import requests
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.logs_aggregate_request import LogsAggregateRequest
from datadog_api_client.v2.model.logs_aggregate_request_page import (
    LogsAggregateRequestPage,
)
from datadog_api_client.v2.model.logs_compute import LogsCompute
from datadog_api_client.v2.model.logs_compute_aggregation_type import (
    LogsComputeAggregationType,
)
from datadog_api_client.v2.model.logs_group_by import LogsGroupBy
from datadog_api_client.v2.model.logs_query_filter import LogsQueryFilter
from datadog_api_client.v2.model.logs_sort import LogsSort
from datadog_api_client.v2.model.logs_list_request import LogsListRequest
from datadog_api_client.v2.model.logs_list_request_page import LogsListRequestPage


DATADOG_SITE = os.getenv("DATADOG_SITE", "datadoghq.com")
DATADOG_API_KEY = os.getenv("DATADOG_API_KEY", "")
DATADOG_APP_KEY = os.getenv("DATADOG_APP_KEY", "")
DATADOG_LOGS_HTTP_URL = f"https://http-intake.logs.{DATADOG_SITE}/api/v2/logs"


def _configuration() -> Configuration:
    configuration = Configuration()
    configuration.server_variables["site"] = DATADOG_SITE
    configuration.api_key["apiKeyAuth"] = DATADOG_API_KEY
    configuration.api_key["appKeyAuth"] = DATADOG_APP_KEY
    return configuration


def get_logs_api() -> LogsApi:
    return LogsApi(ApiClient(_configuration()))


def submit_logs(events: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    response = requests.post(
        DATADOG_LOGS_HTTP_URL,
        headers={
            "Content-Type": "application/json",
            "DD-API-KEY": DATADOG_API_KEY,
        },
        json=list(events),
        timeout=30,
    )
    response.raise_for_status()
    return {
        "status_code": response.status_code,
        "provider": "Datadog",
        "endpoint": DATADOG_LOGS_HTTP_URL,
    }


def list_logs(
    *,
    query: str,
    start: str,
    end: str,
    limit: int = 50,
    sort: LogsSort = LogsSort.TIMESTAMP_DESCENDING,
) -> Any:
    body = LogsListRequest(
        filter=LogsQueryFilter(
            query=query,
            _from=start,
            to=end,
        ),
        sort=sort,
        page=LogsListRequestPage(limit=limit),
    )
    with ApiClient(_configuration()) as api_client:
        api = LogsApi(api_client)
        return api.list_logs(body=body)


def aggregate_logs_by_status(
    *, query: str, start: str, end: str, limit: int = 10
) -> Any:
    body = LogsAggregateRequest(
        compute=[
            LogsCompute(
                aggregation=LogsComputeAggregationType.COUNT,
            )
        ],
        filter=LogsQueryFilter(query=query, _from=start, to=end),
        group_by=[LogsGroupBy(facet="status", limit=limit)],
        page=LogsAggregateRequestPage(limit=limit),
    )
    with ApiClient(_configuration()) as api_client:
        api = LogsApi(api_client)
        return api.aggregate_logs(body=body)


def openai_headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY', '')}",
        "Content-Type": "application/json",
    }


def openai_post(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.post(
        f"https://api.openai.com/v1/{path}",
        headers=openai_headers(),
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def cohere_headers() -> Dict[str, str]:
    return {
        "Authorization": f"Bearer {os.getenv('COHERE_API_KEY', '')}",
        "Content-Type": "application/json",
    }


def cohere_post(path: str, payload: Dict[str, Any]) -> Dict[str, Any]:
    response = requests.post(
        f"https://api.cohere.com/v1/{path}",
        headers=cohere_headers(),
        json=payload,
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def google_translate_headers() -> Dict[str, str]:
    return {"Content-Type": "application/json"}


def google_translate(
    text: str, target_language: str, source_language: Optional[str] = None
) -> Dict[str, Any]:
    api_key = os.getenv("GOOGLE_CLOUD_API_KEY", "")
    params = {"key": api_key}
    body: Dict[str, Any] = {
        "q": text,
        "target": target_language,
        "format": "text",
    }
    if source_language:
        body["source"] = source_language
    response = requests.post(
        "https://translation.googleapis.com/language/translate/v2",
        params=params,
        headers=google_translate_headers(),
        json=body,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
