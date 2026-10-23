import os
from datetime import datetime, timedelta

from observability_client import get_datadog_logs_client
from observability_models import LogQueryResult

from datadog_api_client.v2.model.logs_list_request import LogsListRequest
from datadog_api_client.v2.model.logs_list_request_page import LogsListRequestPage
from datadog_api_client.v2.model.logs_sort import LogsSort
from datadog_api_client.v2.model.logs_list_request_time import LogsListRequestTime

def fetch_recent_logs(query: str, time_range_minutes: int = 60, limit: int = 100):
    """Retrieves recent log results from Datadog filtered by field values and time range."""
    client = get_datadog_logs_client()

    now = datetime.utcnow()
    start_time = now - timedelta(minutes=time_range_minutes)

    body = LogsListRequest(
        filter=LogsListRequestTime(
            _from=start_time.isoformat(),
            to=now.isoformat(),
            query=query,
        ),
        page=LogsListRequestPage(limit=limit),
        sort=LogsSort.TIMESTAMP_DESCENDING,
    )

    try:
        api_response = client.list_logs(body=body)
        
        results = []
        if api_response.data:
            for log_entry in api_response.data:
                results.append({
                    "id": log_entry.id,
                    "timestamp": log_entry.attributes.timestamp.isoformat(),
                    "host": log_entry.attributes.host if log_entry.attributes.host else "N/A",
                    "service": log_entry.attributes.service if log_entry.attributes.service else "N/A",
                    "status": log_entry.attributes.status if log_entry.attributes.status else "N/A",
                    "message": log_entry.attributes.message
                })

        log_query_result = LogQueryResult(results)
        print(f"Found {len(results)} recent logs matching query '{{query}}' in the last {time_range_minutes} minutes from Datadog.")
        print(log_query_result.to_json())
        return log_query_result

    except Exception as e:
        print(f"Error fetching logs from Datadog: {e}")
        return LogQueryResult([])

if __name__ == "__main__":
    # Example usage
    # Ensure DATADOG_API_KEY and DATADOG_APPLICATION_KEY environment variables are set.

    # Example 1: Fetch all logs with severity error
    fetch_recent_logs(query="status:error", time_range_minutes=120)

    # Example 2: Fetch logs from a specific service
    fetch_recent_logs(query="service:my-web-app AND env:production", time_range_minutes=30)

    # Example 3: Fetch logs with a specific message keyword
    fetch_recent_logs(query="message:""User login failed""", time_range_minutes=60, limit=50)
