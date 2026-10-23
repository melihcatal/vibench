from observability_client import ObservabilityClient
from observability_models import LogQuery
from datetime import datetime, timedelta, timezone


def query_error_logs(
    time_range_minutes: int = 60, severity: str = "ERROR"
):  # Default to last 60 minutes and ERROR severity
    client = ObservabilityClient()
    logging_client = client.get_logging_client()

    now = datetime.now(timezone.utc)
    # Calculate the timestamp for the start of the desired time range
    # Google Cloud Logging expects RFC3339 format for timestamps
    start_time = now - timedelta(minutes=time_range_minutes)

    # Construct the filter string
    # Using resource.type="global" is a common default, adjust if logs are associated with specific resources
    filter_string = f'severity = "{severity}" AND timestamp >= "{start_time.isoformat(timespec="seconds")}Z"'
    print(f"Using filter: {filter_string}")

    log_query = LogQuery(filter_string=filter_string, order_by="timestamp desc")

    entries = logging_client.list_entries(
        filter_=log_query.filter_string,
        order_by=log_query.order_by,
        page_size=log_query.limit,
    )

    error_logs = []
    for entry in entries:
        # Convert Protobuf timestamp to Python datetime object for easier handling
        timestamp_dt = (
            entry.timestamp.isoformat(timespec="seconds") if entry.timestamp else "N/A"
        )

        # Extract relevant fields from the log entry
        log_data = {
            "timestamp": timestamp_dt,
            "severity": entry.severity,
            "log_name": entry.log_name,
            "resource_type": entry.resource.type if entry.resource else "N/A",
            "text_payload": entry.text_payload if entry.text_payload else None,
            "json_payload": entry.json_payload if entry.json_payload else None,
            "labels": entry.labels if entry.labels else None,
            "insert_id": entry.insert_id,
        }
        error_logs.append(log_data)

    return error_logs


if __name__ == "__main__":
    # Example usage: query error logs from the last 30 minutes
    recent_errors = query_error_logs(time_range_minutes=30, severity="ERROR")
    if recent_errors:
        print(f"Found {len(recent_errors)} recent error logs:")
        for log in recent_errors:
            print(log)
    else:
        print("No error logs found in the specified time range.")
