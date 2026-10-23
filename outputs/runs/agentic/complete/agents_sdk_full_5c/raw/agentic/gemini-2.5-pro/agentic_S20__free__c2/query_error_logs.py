from datetime import datetime, timedelta, timezone
from typing import List
from observability_client import logging_client, get_gcp_project_id
from observability_models import LogQueryResult

def query_recent_errors(hours: int = 24) -> List[LogQueryResult]:
    """
    Queries for ERROR-level logs in the last N hours.

    Args:
        hours: The number of hours to look back.

    Returns:
        A list of LogQueryResult objects.
    """
    if not logging_client:
        print("Logging client not available. Skipping query.")
        return []

    project_id = get_gcp_project_id()
    query_client = logging_client.get_query_client()

    # Define the time range
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=hours)

    # Format timestamps for the filter
    start_str = start_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
    end_str = end_time.strftime('%Y-%m-%dT%H:%M:%S.%fZ')

    # Construct the filter
    # This filter looks for logs with severity 'ERROR' within the time range.
    log_filter = f"""
    severity="ERROR"
    AND timestamp >= "{start_str}"
    AND timestamp <= "{end_str}"
    """

    print(f"Executing query for error logs in the last {hours} hours...")

    request = {
        "resource_names": [f"projects/{project_id}"],
        "filter": log_filter,
        "order_by": "timestamp desc",
        "page_size": 100,
    }

    results = []
    try:
        # The list_log_entries method returns an iterator
        pages = query_client.list_log_entries(request=request)
        for entry in pages:
            log_item = LogQueryResult(
                timestamp=str(entry.timestamp),
                severity=entry.severity.name,
                message=entry.json_payload.get("message", str(entry.text_payload or "N/A")),
                payload=dict(entry.json_payload),
                trace_id=entry.trace
            )
            results.append(log_item)
    except Exception as e:
        print(f"An error occurred during the query: {e}")
        return []

    return results

if __name__ == "__main__":
    try:
        error_logs = query_recent_errors(hours=24)
        if error_logs:
            print(f"\nFound {len(error_logs)} error logs in the last 24 hours.")
            for log in error_logs[:5]:  # Print first 5
                print(f"- {log.timestamp} [{log.severity}]: {log.message}")
        else:
            print("No error logs found in the specified time range.")
    except Exception as e:
        print(f"Failed to execute query: {e}")
