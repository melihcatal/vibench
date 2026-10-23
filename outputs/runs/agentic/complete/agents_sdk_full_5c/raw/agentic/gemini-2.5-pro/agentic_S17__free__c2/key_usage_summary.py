from datadog_api_client.v2.model.logs_list_request import LogsListRequest
from datadog_api_client.v2.model.logs_list_request_page import LogsListRequestPage
from datadog_api_client.v2.model.logs_query_filter import LogsQueryFilter
from security_client import get_datadog_logs_api

def get_key_usage_from_datadog(query: str, time_offset_ms: int = 3600000):
    """
    Queries Datadog logs for crypto key usage events.

    Args:
        query: The Datadog log query string (e.g., 'source:cloudtrail eventName:Encrypt').
        time_offset_ms: Time window in milliseconds to look back.
    """
    api_instance = get_datadog_logs_api()

    filter_query = query
    filter_from = "now-1h"
    filter_to = "now"

    body = LogsListRequest(
        filter=LogsQueryFilter(
            query=filter_query,
            _from=filter_from,
            to=filter_to,
        ),
        page=LogsListRequestPage(
            limit=10,
        ),
    )

    try:
        # Provider-specific call to Datadog Logs API
        api_response = api_instance.list_logs(body=body)
        return [log.attributes.message for log in api_response.data]
    except Exception as e:
        print(f"Error querying Datadog API: {e}")
        return []
