import os
from datetime import datetime, timezone, timedelta
from datadog_api_client import ApiClient, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.logs_list_request import LogsListRequest
from datadog_api_client.v2.model.logs_list_request_page import LogsListRequestPage
from datadog_api_client.v2.model.logs_sort import LogsSort
from datadog_api_client.v2.model.logs_query_filter import LogsQueryFilter
from observability_models import ErrorLogQuery, ErrorLogEntry, ErrorLogQueryResponse
from observability_client import get_datadog_config, normalize_datadog_log_entry


def query_error_logs(
    service: str = "*",
    severity: str = "error",
    hours_back: int = 24,
    limit: int = 100,
    source: str | None = None,
) -> ErrorLogQueryResponse:
    api_key = os.environ.get("DD_API_KEY")
    app_key = os.environ.get("DD_APP_KEY")
    if not api_key or not app_key:
        raise ValueError("DD_API_KEY and DD_APP_KEY environment variables are required")

    config = get_datadog_config(api_key, app_key)
    now = datetime.now(timezone.utc)
    from_ts = now - timedelta(hours=hours_back)

    query_parts = [f"status:{severity}"]
    if service and service != "*":
        query_parts.append(f"service:{service}")
    if source:
        query_parts.append(f"source:{source}")

    query_filter = LogsQueryFilter(query=" ".join(query_parts), _from=from_ts, to=now)
    page = LogsListRequestPage(limit=limit)

    request = LogsListRequest(
        filter=query_filter,
        sort=LogsSort.TIMESTAMP_DESCENDING,
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
                ErrorLogEntry(
                    event_id=normalized.get("event_id", ""),
                    timestamp=normalized.get("timestamp", ""),
                    message=normalized.get("message", ""),
                    level=normalized.get("level", severity),
                    service=normalized.get("service", ""),
                    source=normalized.get("source", ""),
                    attributes=normalized.get("attributes", {}),
                )
            )

    return ErrorLogQueryResponse(
        query=ErrorLogQuery(
            service=service,
            severity=severity,
            hours_back=hours_back,
            source=source,
        ),
        total_found=len(entries),
        entries=entries,
        queried_at=now.isoformat(),
    )


if __name__ == "__main__":
    result = query_error_logs(
        service="payment-gateway",
        severity="error",
        hours_back=6,
        limit=50,
    )
    print(result.model_dump_json(indent=2))
