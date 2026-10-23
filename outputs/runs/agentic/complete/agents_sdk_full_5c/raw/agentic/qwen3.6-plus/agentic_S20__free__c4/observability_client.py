"""
Local configuration and client helper utilities for Managed Log Query / Log Ingestion.

Provides Datadog API client wrapper with authentication, log ingestion,
query execution, and response handling utilities.
"""

from __future__ import annotations

import json
import os
import time
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, List, Optional

from datadog_api_client import Configuration
from datadog_api_client.v1.api.logs_api import LogsApi
from datadog_api_client.v1.api.logs_indexes_api import LogsIndexesApi
from datadog_api_client.v1.model.logs_list_request import LogsListRequest
from datadog_api_client.v1.model.logs_list_request_time import LogsListRequestTime
from datadog_api_client.v1.model.logs_list_request_filter import LogsListRequestFilter
from datadog_api_client.v1.model.logs_list_request_page import LogsListRequestPage
from datadog_api_client.v2.api.logs_api import LogsApi as LogsApiV2
from datadog_api_client.v2.model.http_log import HTTPLog
from datadog_api_client.v2.model.http_logs import HTTPLogs

from observability_models import (
    StructuredLogEvent,
    LogQueryFilter,
    LogEntry,
    QueryResult,
    LogLevel,
)

DATADOG_API_HOST = "https://api.datadoghq.com"


def load_datadog_config() -> Configuration:
    """Load Datadog API configuration from environment variables."""
    api_key = os.environ.get("DATADOG_API_KEY", "")
    app_key = os.environ.get("DATADOG_APP_KEY", "")
    api_host = os.environ.get("DATADOG_API_HOST", DATADOG_API_HOST)

    if not api_key:
        raise ValueError(
            "DATADOG_API_KEY environment variable is required. "
            "Set it to your Datadog API key from "
            "https://app.datadoghq.com/organization-settings/api-keys"
        )

    config = Configuration()
    config.api_key = {"apiKeyAuth": api_key}
    if app_key:
        config.api_key["appKeyAuth"] = app_key
    config.host = api_host
    return config


def create_datadog_v2_client() -> LogsApiV2:
    """Create a Datadog v2 Logs API client for log ingestion."""
    config = load_datadog_config()
    with config:
        api_client = config.create_api_client()
        return LogsApiV2(api_client)


def create_datadog_v1_client() -> LogsApi:
    """Create a Datadog v1 Logs API client for log search/queries."""
    config = load_datadog_config()
    with config:
        api_client = config.create_api_client()
        return LogsApi(api_client)


def ingest_log_event(event: StructuredLogEvent) -> Dict[str, Any]:
    """Ingest a single structured log event to Datadog Logs.

    Uses the Datadog v2 HTTP Logs API endpoint at api.datadoghq.com.
    The concrete model for ingestion is the HTTPLog/HTTPLogs schema.
    """
    client = create_datadog_v2_client()
    payload = event.to_datadog_payload()

    http_log = HTTPLog(
        ddsource=payload.get("ddsource", "python"),
        ddtags=payload.get("ddtags", ""),
        hostname=payload.get("hostname", ""),
        service=payload.get("service", ""),
        message=payload.get("message", ""),
        status=payload.get("status", "info"),
        **{k: v for k, v in payload.items()
           if k not in ("ddsource", "ddtags", "hostname", "service", "message", "status")},
    )
    http_logs = HTTPLogs(logs=[http_log])

    response = client.submit_log(body=http_logs)
    return {"status": "accepted", "event_id": event.correlation_id}


def ingest_log_events(events: List[StructuredLogEvent]) -> Dict[str, Any]:
    """Ingest multiple structured log events to Datadog Logs in a batch."""
    client = create_datadog_v2_client()
    http_logs_list = []

    for event in events:
        payload = event.to_datadog_payload()
        http_log = HTTPLog(
            ddsource=payload.get("ddsource", "python"),
            ddtags=payload.get("ddtags", ""),
            hostname=payload.get("hostname", ""),
            service=payload.get("service", ""),
            message=payload.get("message", ""),
            status=payload.get("status", "info"),
            **{k: v for k, v in payload.items()
               if k not in ("ddsource", "ddtags", "hostname", "service", "message", "status")},
        )
        http_logs_list.append(http_log)

    http_logs = HTTPLogs(logs=http_logs_list)
    response = client.submit_log(body=http_logs)
    return {"status": "accepted", "count": len(events)}


def query_logs(
    filter_query: LogQueryFilter,
    index: str = "main",
) -> QueryResult:
    """Query logs from Datadog using the v1 Logs Search API.

    Connects to api.datadoghq.com via the datadog-api-client SDK.
    """
    client = create_datadog_v1_client()

    datadog_query = filter_query.to_datadog_query()

    if filter_query.time_from is None:
        filter_query.time_from = datetime.now(timezone.utc) - timedelta(minutes=60)
    if filter_query.time_to is None:
        filter_query.time_to = datetime.now(timezone.utc)

    from_ts = int(filter_query.time_from.timestamp())
    to_ts = int(filter_query.time_to.timestamp())

    time_filter = LogsListRequestTime(
        _from=from_ts,
        to=to_ts,
    )
    list_filter = LogsListRequestFilter(
        query=datadog_query,
        indexes=[index],
    )
    page = LogsListRequestPage(
        limit=filter_query.limit,
    )

    body = LogsListRequest(
        filter=list_filter,
        sort=filter_query.sort,
        time=time_filter,
        page=page,
    )

    start_time = time.monotonic()
    response = client.list_logs(body=body)
    elapsed_ms = (time.monotonic() - start_time) * 1000

    entries = []
    for log_hit in response.get("logs", []):
        entry = LogEntry.from_datadog_response(log_hit)
        entries.append(entry)

    total = response.get("matching_logs_count", len(entries))

    return QueryResult(
        entries=entries,
        total_count=total,
        query_string=datadog_query,
        elapsed_ms=elapsed_ms,
    )


def query_logs_paginated(
    filter_query: LogQueryFilter,
    index: str = "main",
    max_pages: int = 5,
) -> QueryResult:
    """Query logs with pagination support for larger result sets."""
    client = create_datadog_v1_client()

    datadog_query = filter_query.to_datadog_query()

    if filter_query.time_from is None:
        filter_query.time_from = datetime.now(timezone.utc) - timedelta(minutes=60)
    if filter_query.time_to is None:
        filter_query.time_to = datetime.now(timezone.utc)

    from_ts = int(filter_query.time_from.timestamp())
    to_ts = int(filter_query.time_to.timestamp())

    time_filter = LogsListRequestTime(_from=from_ts, to=to_ts)
    list_filter = LogsListRequestFilter(query=datadog_query, indexes=[index])
    page = LogsListRequestPage(limit=min(filter_query.limit, 100))

    body = LogsListRequest(
        filter=list_filter,
        sort=filter_query.sort,
        time=time_filter,
        page=page,
    )

    all_entries: List[LogEntry] = []
    total_count = 0
    start_time = time.monotonic()

    for page_num in range(max_pages):
        response = client.list_logs(body=body)
        total_count = response.get("matching_logs_count", 0)

        for log_hit in response.get("logs", []):
            entry = LogEntry.from_datadog_response(log_hit)
            all_entries.append(entry)

        response_id = response.get("response", {}).get("id")
        if not response_id or len(response.get("logs", [])) == 0:
            break

        page = LogsListRequestPage(limit=min(filter_query.limit, 100), cursor=response_id)
        body = LogsListRequest(
            filter=list_filter,
            sort=filter_query.sort,
            time=time_filter,
            page=page,
        )

    elapsed_ms = (time.monotonic() - start_time) * 1000

    return QueryResult(
        entries=all_entries,
        total_count=total_count,
        query_string=datadog_query,
        elapsed_ms=elapsed_ms,
    )


def get_log_entry_by_id(log_id: str, index: str = "main") -> Optional[LogEntry]:
    """Retrieve a single log entry by its ID from Datadog."""
    client = create_datadog_v1_client()
    try:
        response = client.get_log(log_id, index=index)
        return LogEntry.from_datadog_response(response)
    except Exception:
        return None
