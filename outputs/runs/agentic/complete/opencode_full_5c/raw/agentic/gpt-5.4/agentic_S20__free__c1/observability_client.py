from __future__ import annotations

from dataclasses import asdict
import os
from typing import Iterable

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.http_log import HTTPLog
from datadog_api_client.v2.model.http_log_item import HTTPLogItem
from datadog_api_client.v2.model.http_log_items import HTTPLogItems
from datadog_api_client.v2.model.logs_list_request import LogsListRequest
from datadog_api_client.v2.model.logs_list_request_page import LogsListRequestPage
from datadog_api_client.v2.model.logs_query_filter import LogsQueryFilter
from datadog_api_client.v2.model.logs_sort import LogsSort

from observability_models import LogEvent, LogQuery, QueryResult, normalize_datadog_log


DATADOG_API_HOST = "https://api.datadoghq.com"


def load_datadog_configuration() -> Configuration:
    configuration = Configuration()
    configuration.server_variables["site"] = os.getenv("DD_SITE", "datadoghq.com")
    configuration.api_key["apiKeyAuth"] = os.environ["DD_API_KEY"]
    configuration.api_key["appKeyAuth"] = os.environ["DD_APP_KEY"]
    return configuration


def create_logs_api() -> tuple[ApiClient, LogsApi]:
    client = ApiClient(load_datadog_configuration())
    return client, LogsApi(client)


def build_http_log_item(
    event: LogEvent, ddsource: str = "python", ddtags: str | None = None
) -> HTTPLogItem:
    return HTTPLogItem(event.to_datadog(ddsource=ddsource, ddtags=ddtags))


def send_logs(
    events: Iterable[LogEvent], ddsource: str = "python", ddtags: str | None = None
) -> dict:
    client, api = create_logs_api()
    body = HTTPLog(
        [
            build_http_log_item(event, ddsource=ddsource, ddtags=ddtags)
            for event in events
        ]
    )
    try:
        response = api.submit_log(body=body, content_encoding="gzip")
        if hasattr(response, "to_dict"):
            return response.to_dict()
        return asdict(response)
    finally:
        client.close()


def query_logs(query: LogQuery) -> QueryResult:
    client, api = create_logs_api()
    body = LogsListRequest(
        filter=LogsQueryFilter(**query.to_datadog_filter()),
        page=LogsListRequestPage(**query.to_datadog_page()),
        sort=LogsSort(query.to_datadog_sort()),
    )
    try:
        response = api.list_logs(body=body)
        records = [
            normalize_datadog_log(item)
            for item in list(getattr(response, "data", []) or [])
        ]
        meta = getattr(response, "meta", None)
        total = getattr(meta, "page", None)
        total_count = getattr(total, "after", None) if total is not None else None
        return QueryResult(records=records, total=total_count)
    finally:
        client.close()
