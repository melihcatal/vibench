from datetime import datetime, timedelta, timezone
from datadog_api_client.api import logs_api
from datadog_api_client.model.logs_list_request import LogsListRequest
from datadog_api_client.model.logs_list_request_page import LogsListRequestPage
from datadog_api_client.model.logs_query_filter import LogsQueryFilter
from datadog_api_client.model.logs_sort import LogsSort


from security_client import get_datadog_api_client
from security_models import AuditSummaryRequest


def get_key_usage_summary(request: AuditSummaryRequest) -> list:
    """
    Queries Datadog Logs for crypto key usage events.

    Args:
        request: An AuditSummaryRequest containing the query and timeframe.

    Returns:
        A list of log entries matching the query.
    """
    api_client = get_datadog_api_client()
    logs_api_instance = logs_api.LogsApi(api_client)

    now = datetime.now(timezone.utc)
    from_time = now - timedelta(hours=request.timeframe_hours)

    filter_query = request.query
    filter_from = from_time
    filter_to = now

    body = LogsListRequest(
        filter=LogsQueryFilter(
            query=filter_query,
            _from=filter_from,
            to=filter_to,
        ),
        page=LogsListRequestPage(limit=100),
        sort=LogsSort("timestamp"),
    )

    try:
        response = logs_api_instance.list_logs(body)
        return response.data
    except Exception as e:
        print(f"Error querying Datadog logs: {e}")
        return []
