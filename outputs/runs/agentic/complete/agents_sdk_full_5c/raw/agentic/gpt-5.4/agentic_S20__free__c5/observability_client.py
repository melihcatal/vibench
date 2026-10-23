from __future__ import annotations

import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.logs_aggregate_sort import LogsAggregateSort
from datadog_api_client.v2.model.logs_list_request import LogsListRequest
from datadog_api_client.v2.model.logs_list_request_page import LogsListRequestPage
from datadog_api_client.v2.model.logs_query_filter import LogsQueryFilter
from datadog_api_client.v2.model.http_log import HTTPLog
from datadog_api_client.v2.model.http_log_item import HTTPLogItem
from datadog_api_client.v2.model.content_encoding import ContentEncoding

from observability_models import LogQueryRequest


DATADOG_SITE = os.getenv("DATADOG_SITE", "datadoghq.com")
DATADOG_API_KEY = os.getenv("DATADOG_API_KEY")
DATADOG_APP_KEY = os.getenv("DATADOG_APP_KEY")


def get_datadog_configuration() -> Configuration:
    configuration = Configuration()
    configuration.server_variables["site"] = DATADOG_SITE
    configuration.api_key["apiKeyAuth"] = DATADOG_API_KEY
    configuration.api_key["appKeyAuth"] = DATADOG_APP_KEY
    return configuration


def get_logs_api() -> LogsApi:
    api_client = ApiClient(get_datadog_configuration())
    return LogsApi(api_client)


def make_http_log_item(payload: dict) -> HTTPLogItem:
    return HTTPLogItem(payload)


def make_http_log(body: list[HTTPLogItem]) -> HTTPLog:
    return HTTPLog(body)


def default_time_range(minutes: int = 15) -> tuple[datetime, datetime]:
    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=minutes)
    return start, end


def build_logs_list_request(request: LogQueryRequest) -> LogsListRequest:
    sort = LogsAggregateSort.TIMESTAMP_DESC if request.to_datadog_sort() == "desc" else LogsAggregateSort.TIMESTAMP_ASC
    return LogsListRequest(
        filter=LogsQueryFilter(**request.to_datadog_filter()),
        page=LogsListRequestPage(**request.to_datadog_page()),
        sort=sort,
    )


def ensure_required_credentials(require_app_key: bool = True) -> None:
    if not DATADOG_API_KEY:
        raise ValueError("DATADOG_API_KEY is required")
    if require_app_key and not DATADOG_APP_KEY:
        raise ValueError("DATADOG_APP_KEY is required")
