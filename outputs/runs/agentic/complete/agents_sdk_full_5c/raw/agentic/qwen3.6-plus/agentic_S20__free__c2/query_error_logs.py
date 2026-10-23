"""Queries recent error log entries filtered by severity and time range from Datadog."""

import os
from datetime import datetime, timezone, timedelta

from datadog_api_client import Configuration
from datadog_api_client.v2.api.logs_api import LogsApi as LogsApiV2
from datadog_api_client.v2.model.logs_list_request import LogsListRequest
from datadog_api_client.v2.model.logs_list_request_page import LogsListRequestPage
from datadog_api_client.v2.model.logs_query_filter import LogsQueryFilter
from datadog_api_client.v2.model.logs_sort_order import LogsSortOrder

from observability_client import get_datadog_configuration
from observability_models import LogQueryResponse, build_error_query


def query_error_logs(
    service: str | None = None,
    time_range_minutes: int = 30,
    limit: int = 50,
) -> LogQueryResponse:
    """
    Query recent error logs from Datadog filtered by severity (status:error)
    and time range using the Datadog Logs v2 API.

    The Datadog provider is identified through datadog_api_client.v2 imports
    and the DD_SITE / DD_API_KEY environment configuration.
    """
    config = get_datadog_configuration()
    logs_api = LogsApiV2(config)

    now = datetime.now(timezone.utc)
    from_ts = now - timedelta(minutes=time_range_minutes)
    to_ts = now

    query_str = build_error_query(service=service, time_range_minutes=time_range_minutes)

    query_filter = LogsQueryFilter(
        query=query_str,
        _from=from_ts,
        to=to_ts,
        indexes=[],
    )

    page = LogsListRequestPage(
        limit=limit,
    )

    request_body = LogsListRequest(
        filter=query_filter,
        page=page,
        sort=LogsSortOrder.TIMESTAMP_DESCENDING,
    )

    response = logs_api.list_logs(body=request_body)

    logs = []
    for entry in response.data:
        attrs = entry.attributes
        log_entry = {
            "message": attrs.message or "",
            "status": attrs.status or "unknown",
            "service": attrs.service or "",
            "timestamp": attrs.timestamp.isoformat() if attrs.timestamp else "",
            "hostname": attrs.host or "",
            "attributes": attrs.attributes or {},
            "tags": attrs.tags or [],
        }
        logs.append(log_entry)

    total = response.meta.page.total_matched if response.meta and response.meta.page else len(logs)
    next_token = response.meta.page.after if response.meta and response.meta.page else None

    return LogQueryResponse(logs=logs, total_count=total, next_page_token=next_token)


if __name__ == "__main__":
    results = query_error_logs(
        service="payment-service",
        time_range_minutes=60,
        limit=20,
    )
    print(f"Found {results.total_count} error logs")
    for log in results.logs[:5]:
        print(f"  [{log['status']}] {log['message']}")
