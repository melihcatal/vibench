from typing import List
from observability_client import get_datadog_client
from observability_models import LogQueryResponse, LogQueryFilter

def find_recent_error_logs() -> List[LogQueryResponse]:
    """
    Queries Datadog for recent logs with 'error' status.

    Returns:
        A list of LogQueryResponse objects.
    """
    logs_api = get_datadog_client()
    
    # Define a filter for error logs in the last hour
    filters = LogQueryFilter(
        query="status:error",
        from_time="now-1h",
        to_time="now",
        limit=50
    )

    try:
        response = logs_api.list_logs(
            filter_query=filters.query,
            filter_from=filters.from_time,
            filter_to=filters.to_time,
            page_limit=filters.limit
        )

        results = [
            LogQueryResponse(
                id=log.id,
                timestamp=log.attributes.timestamp,
                message=log.attributes.message,
                attributes=log.attributes.attributes
            )
            for log in response.data
        ]
        return results
    except Exception as e:
        print(f"Error querying logs from Datadog: {e}")
        return []
