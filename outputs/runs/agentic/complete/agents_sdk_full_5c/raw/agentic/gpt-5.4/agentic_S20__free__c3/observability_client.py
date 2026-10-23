from __future__ import annotations

import os
from typing import Any, Dict, List

from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.http_log import HTTPLog
from datadog_api_client.v2.model.http_log_item import HTTPLogItem
from datadog_api_client.v2.model.content_encoding import ContentEncoding
from datadog_api_client.v2.model.logs_list_request import LogsListRequest
from datadog_api_client.v2.model.logs_list_request_page import LogsListRequestPage
from datadog_api_client.v2.model.logs_query_filter import LogsQueryFilter
from datadog_api_client.v2.model.logs_sort import LogsSort

from observability_models import LogEvent, LogQueryRequest, LogQueryResponse, normalize_datadog_log


DATADOG_API_KEY_ENV = "DATADOG_API_KEY"
DATADOG_APP_KEY_ENV = "DATADOG_APP_KEY"
DATADOG_SITE_ENV = "DATADOG_SITE"
DEFAULT_DATADOG_SITE = "datadoghq.com"


def build_configuration() -> Configuration:
    configuration = Configuration()
    configuration.server_variables["site"] = os.getenv(DATADOG_SITE_ENV, DEFAULT_DATADOG_SITE)
    configuration.api_key["apiKeyAuth"] = os.environ[DATADOG_API_KEY_ENV]
    configuration.api_key["appKeyAuth"] = os.environ[DATADOG_APP_KEY_ENV]
    return configuration


def create_logs_api_client() -> tuple[ApiClient, LogsApi]:
    api_client = ApiClient(build_configuration())
    return api_client, LogsApi(api_client)


def submit_log_events(events: List[LogEvent]) -> Any:
    api_client, logs_api = create_logs_api_client()
    body = HTTPLog(
        [
            HTTPLogItem(
                ddsource="python",
                ddtags=f"service:{event.service},env:{event.environment or 'unknown'},level:{event.level.lower()}",
                hostname=os.getenv("HOSTNAME", "local-host"),
                service=event.service,
                message=event.to_json(),
            )
            for event in events
        ]
    )
    try:
        return logs_api.submit_log(content_encoding=ContentEncoding.GZIP, body=body)
    finally:
        api_client.close()


def query_logs(request: LogQueryRequest) -> LogQueryResponse:
    api_client, logs_api = create_logs_api_client()
    body = LogsListRequest(
        filter=LogsQueryFilter(
            query=request.query,
            _from=request.from_time,
            to=request.to_time,
        ),
        sort=LogsSort.TIMESTAMP_DESCENDING,
        page=LogsListRequestPage(limit=request.limit),
    )
    try:
        result = logs_api.list_logs(body=body)
        records = [normalize_datadog_log(item.to_dict()) for item in result.data or []]
        return LogQueryResponse(records=records)
    finally:
        api_client.close()


def build_field_query(filters: Dict[str, Any]) -> str:
    parts = []
    for key, value in filters.items():
        if value is None:
            continue
        escaped = str(value).replace('"', '\\"')
        parts.append(f'@{key}:"{escaped}"')
    return " AND ".join(parts) if parts else "*"
