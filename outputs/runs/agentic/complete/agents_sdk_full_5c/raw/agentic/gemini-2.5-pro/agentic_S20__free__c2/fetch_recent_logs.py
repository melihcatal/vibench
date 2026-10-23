from datetime import datetime, timedelta, timezone
from typing import List, Dict, Any
from observability_client import logging_client, get_gcp_project_id
from observability_models import LogQueryResult

def fetch_logs_by_fields(
    filters: Dict[str, Any],
    hours: int = 1,
    limit: int = 100
) -> List[LogQueryResult]:
    """
    Fetches recent logs filtered by specific field values in the JSON payload.

    Args:
        filters: A dictionary of field keys and values to filter on.
                 Example: {"jsonPayload.user.id": "user-9876"}
        hours: The number of hours to look back.
        limit: The maximum number of log entries to return.

    Returns:
        A list of LogQueryResult objects matching the criteria.
    """
    if not logging_client:
        print("Logging client not available. Skipping query.")
        return []

    project_id = get_gcp_project_id()
    query_client = logging_client.get_query_client()

    # Define the time range
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=hours)
    start_str = start_time.isoformat("T") + "Z"
    end_str = end_time.isoformat("T") + "Z"

    # Construct the filter from the dictionary
    filter_parts = [f'timestamp >= "{start_str}"', f'timestamp <= "{end_str}"']
    for key, value in filters.items():
        # Add quotes for string values
        filter_value = f'"{value}"' if isinstance(value, str) else value
        filter_parts.append(f"{key}={filter_value}")

    log_filter = " AND ".join(filter_parts)

    print(f"Executing query with filter: {log_filter}")

    request = {
        "resource_names": [f"projects/{project_id}"],
        "filter": log_filter,
        "order_by": "timestamp desc",
        "page_size": limit,
    }

    results = []
    try:
        response = query_client.list_log_entries(request=request)
        for entry in response:
            results.append(
                LogQueryResult(
                    timestamp=str(entry.timestamp),
                    severity=entry.severity.name if entry.severity else "DEFAULT",
                    message=entry.json_payload.get("message", str(entry.text_payload or "N/A")),
                    payload=dict(entry.json_payload) if entry.json_payload else {},
                )
            )
    except Exception as e:
        print(f"An error occurred during the query: {e}")
        return []

    return results

if __name__ == "__main__":
    try:
        # Example: Find logs for a specific user and HTTP status
        search_filters = {
            "jsonPayload.user.id": "user-9876",
            "jsonPayload.httpRequest.status": 200,
        }
        
        recent_logs = fetch_logs_by_fields(filters=search_filters, hours=24)

        if recent_logs:
            print(f"\nFound {len(recent_logs)} matching logs.")
            for log in recent_logs:
                print(f"- {log.timestamp}: {log.message}")
        else:
            print("No logs found matching the specified criteria.")

    except Exception as e:
        print(f"Failed to execute query: {e}")
