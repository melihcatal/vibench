from typing import List, Optional
from observability_client import get_datadog_client
from observability_models import LogQueryResponse, LogQueryFilter

def fetch_logs_by_field(service: str, user_id: Optional[str] = None) -> List[LogQueryResponse]:
    """
    Retrieves recent logs from Datadog, filtered by service and optionally by user ID.

    Args:
        service: The service name to filter by (e.g., 'payment-service').
        user_id: An optional user ID to include in the filter.

    Returns:
        A list of LogQueryResponse objects matching the criteria.
    """
    logs_api = get_datadog_client()
    
    query_parts = [f"service:{service}"]
    if user_id:
        # Assuming user ID is stored in a log attribute like 'usr.id'
        query_parts.append(f"@usr.id:{user_id}")
    
    full_query = " ".join(query_parts)

    filters = LogQueryFilter(
        query=full_query,
        from_time="now-15m",
        to_time="now",
        limit=100
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
        print(f"Error fetching logs from Datadog: {e}")
        return []
