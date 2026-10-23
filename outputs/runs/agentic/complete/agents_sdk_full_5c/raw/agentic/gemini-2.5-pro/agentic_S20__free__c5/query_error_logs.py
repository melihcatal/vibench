import os
from datetime import datetime, timedelta, timezone
from observability_client import get_gcp_logging_client

def query_for_recent_errors():
    """
    Queries Google Cloud Logging for log entries with 'ERROR' severity
    from the last 24 hours.
    """
    try:
        client = get_gcp_logging_client()
        project_id = client.project
        logger_name = os.environ.get("GCP_LOG_NAME", "my_app_logs")

        # Define the time range: last 24 hours
        end_time = datetime.now(timezone.utc)
        start_time = end_time - timedelta(days=1)
        
        # Format timestamps for the filter
        start_rfc3339 = start_time.isoformat()
        end_rfc3339 = end_time.isoformat()

        # Construct a filter for ERROR severity within the time range for a specific log
        filter_str = (
            f'logName="projects/{project_id}/logs/{logger_name}" '
            f'AND severity="ERROR" '
            f'AND timestamp >= "{start_rfc3339}" '
            f'AND timestamp <= "{end_rfc3339}"'
        )

        print(f"Querying for error logs with filter: {filter_str}")

        # Execute the query
        entries = client.list_entries(filter_=filter_str, order_by="timestamp desc", page_size=25)

        print("--- Recent Error Logs ---")
        found_entries = False
        for entry in entries:
            found_entries = True
            payload = entry.payload
            message = payload.get('message', 'N/A') if isinstance(payload, dict) else str(payload)
            print(f"Timestamp: {entry.timestamp}, Message: {message}")
        
        if not found_entries:
            print("No error logs found in the last 24 hours.")
        
        return entries

    except Exception as e:
        print(f"An error occurred during log query: {e}")
        return []

if __name__ == '__main__':
    query_for_recent_errors()
