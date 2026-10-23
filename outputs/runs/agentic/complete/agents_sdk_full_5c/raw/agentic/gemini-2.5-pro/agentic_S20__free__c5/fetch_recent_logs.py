import os
from datetime import datetime, timedelta, timezone
from observability_client import get_gcp_logging_client

def fetch_logs_by_field_value(field: str, value: str, hours: int = 1):
    """
    Retrieves recent logs from Google Cloud Logging filtered by a JSON
    payload field and a time range.

    Args:
        field: The key in the jsonPayload to filter on (e.g., 'jsonPayload.user_id').
        value: The value to match for the given field.
        hours: The number of hours in the past to search.
    """
    try:
        client = get_gcp_logging_client()
        project_id = client.project
        logger_name = os.environ.get("GCP_LOG_NAME", "my_app_logs")
        
        # Define time range
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(hours=hours)
        start_rfc3339 = start_time.isoformat()
        end_rfc3339 = end_time.isoformat()

        # Construct the filter
        # Note: Google Cloud Logging uses dot notation for JSON fields.
        filter_str = (
            f'logName="projects/{project_id}/logs/{logger_name}" '
            f'AND jsonPayload.{field}="{value}" '
            f'AND timestamp >= "{start_rfc3339}" '
            f'AND timestamp <= "{end_rfc3339}"'
        )
        
        print(f"Fetching logs with filter: {filter_str}")

        # Retrieve logs
        entries = client.list_entries(filter_=filter_str, order_by="timestamp desc")

        print(f"--- Logs for {field} = {value} in the last {hours} hour(s) ---")
        found_entries = False
        for entry in entries:
            found_entries = True
            payload = entry.payload
            message = payload.get('message', 'N/A') if isinstance(payload, dict) else str(payload)
            print(f"[{entry.timestamp}] {message} (Trace: {payload.get('trace_id', 'N/A')})")
        
        if not found_entries:
            print("No matching logs found.")

        return entries

    except Exception as e:
        print(f"An error occurred while fetching recent logs: {e}")
        return []

if __name__ == '__main__':
    # Example: Find logs for a specific user.
    # Assumes a log entry with a jsonPayload like {"user_id": "user-12345", ...} exists.
    fetch_logs_by_field_value(field="user_id", value="user-12345", hours=24)
