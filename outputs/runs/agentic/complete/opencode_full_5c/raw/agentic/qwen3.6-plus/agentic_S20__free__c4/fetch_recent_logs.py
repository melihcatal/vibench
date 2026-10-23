import os
from datetime import datetime, timezone, timedelta
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.logs_list_request import LogsListRequest
from datadog_api_client.v2.model.logs_list_request_page import LogsListRequestPage
from datadog_api_client.v2.model.logs_sort import LogsSort
from datadog_api_client.v2.model.logs_query_filter import LogsQueryFilter
from observability_models import LogFetchParams, LogEntry, LogFetchResponse
from observability_client import get_datadog_config, normalize_datadog_log_entry


def fetch_recent_logs(
    service: str = "*",
    field_filters: dict[str, str] | None = None,
    hours_back: int = 1,
    limit: int = 200,
    sort_order: str = "desc",
) -> LogFetchResponse:
    api_key = os.environ.get("DD_API_KEY")
    app_key = os.environ.get("DD_APP_KEY")
    if not api_key or not app_key:
        raise ValueError("DD_API_KEY and DD_APP_KEY environment variables are required")

    config = get_datadog_config(api_key, app_key)
    now = datetime.now(timezone.utc)
    from_ts = now - timedelta(hours=hours_back)

    query_parts = []
    if service and service != "*":
        query_parts.append(f"service:{service}")

    field_filters = field_filters or {}
    for key, value in field_filters.items():
        query_parts.append(f"@{key}:{value}")

    query_string = " ".join(query_parts) if query_parts else "*"
    query_filter = LogsQueryFilter(query=query_string, _from=from_ts, to=now)
    page = LogsListRequestPage(limit=limit)
    sort = (
        LogsSort.TIMESTAMP_DESCENDING
        if sort_order == "desc"
        else LogsSort.TIMESTAMP_ASCENDING
    )

    request = LogsListRequest(
        filter=query_filter,
        sort=sort,
        page=page,
    )

    with ApiClient(configuration=config) as api_client:
        logs_api = LogsApi(api_client)
        response = logs_api.list_logs(body=request)

    entries = []
    if response.data:
        for log_item in response.data:
            normalized = normalize_datadog_log_entry(log_item)
            entries.append(
                LogEntry(
                    event_id=normalized.get("event_id", ""),
                    timestamp=normalized.get("timestamp", ""),
                    message=normalized.get("message", ""),
                    level=normalized.get("level", "info"),
                    service=normalized.get("service", ""),
                    source=normalized.get("source", ""),
                    attributes=normalized.get("attributes", {}),
                )
            )

    params = LogFetchParams(
        service=service,
        field_filters=field_filters,
        hours_back=hours_back,
        limit=limit,
        sort_order=sort_order,
    )

    return LogFetchResponse(
        params=params,
        total_found=len(entries),
        entries=entries,
        fetched_at=now.isoformat(),
    )


if __name__ == "__main__":
    result = fetch_recent_logs(
        service="checkout-api",
        field_filters={"http.status_code": "500", "env": "production"},
        hours_back=2,
        limit=100,
    )
    print(result.model_dump_json(indent=2))
