"""Retrieves recent log results filtered by field values and time range from Datadog."""

import os
from datetime import datetime, timezone, timedelta

from datadog_api_client import Configuration
from datadog_api_client.v2.api.logs_api import LogsApi as LogsApiV2
from datadog_api_client.v2.model.logs_list_request import LogsListRequest
from datadog_api_client.v2.model.logs_list_request_page import LogsListRequestPage
from datadog_api_client.v2.model.logs_query_filter import LogsQueryFilter
from datadog_api_client.v2.model.logs_sort_order import LogsSortOrder

from observability_client import get_datadog_configuration
from observability_models import LogQueryResponse, build_recent_query, compute_time_range


def fetch_recent_logs(
    filters: dict | None = None,
    time_range_minutes: int = 15,
    limit: int = 100,
    service: str | None = None,
    sort_order: str = "timestamp_descending",
) -> LogQueryResponse:
    """
    Fetch recent logs from Datadog using field-value filters and a time range.

    Uses the Datadog Logs v2 API (datadog_api_client.v2) to query logs
    filtered by arbitrary key-value field pairs within the specified time window.
    Provider is identified via datadog_api_client imports and DD_API_KEY config.
    """
    config = get_datadog_configuration()
    logs_api = LogsApiV2(config)

    now = datetime.now(timezone.utc)
    from_ts = now - timedelta(minutes=time_range_minutes)
    to_ts = now

    query_parts = []
    if service:
        query_parts.append(f"service:{service}")
    if filters:
        for key, value in filters.items():
            query_parts.append(f"{key}:{value}")

    query_str = " ".join(query_parts) if query_parts else "*"

    query_filter = LogsQueryFilter(
        query=query_str,
        _from=from_ts,
        to=to_ts,
        indexes=[],
    )

    page = LogsListRequestPage(limit=limit)

    sort_map = {
        "timestamp_descending": LogsSortOrder.TIMESTAMP_DESCENDING,
        "timestamp_ascending": LogsSortOrder.TIMESTAMP_ASCENDING,
    }
    sort = sort_map.get(sort_order, LogsSortOrder.TIMESTAMP_DESCENDING)

    request_body = LogsListRequest(
        filter=query_filter,
        page=page,
        sort=sort,
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
    results = fetch_recent_logs(
        filters={"env": "production", "http.method": "POST"},
        time_range_minutes=30,
        limit=50,
        service="api-gateway",
    )
    print(f"Fetched {results.total_count} logs")
    for log in results.logs[:5]:
        print(f"  [{log['timestamp']}] [{log['status']}] {log['service']}: {log['message']}")
