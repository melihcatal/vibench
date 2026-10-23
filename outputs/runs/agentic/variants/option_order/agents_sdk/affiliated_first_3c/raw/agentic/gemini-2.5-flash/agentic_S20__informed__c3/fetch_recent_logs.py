import os
import datetime
from google.cloud import logging

def fetch_recent_logs(log_name: str, field_filters: dict = None, time_range_minutes: int = 60):
    """Retrieves recent log results filtered by field values and time range from Google Cloud Logging."""
    client = logging.Client()

    now = datetime.datetime.now(datetime.timezone.utc)
    filter_parts = [
        f'logName="projects/{client.project}/logs/{log_name}"',
        f'timestamp>="{now - datetime.timedelta(minutes=time_range_minutes)}"'
    ]

    if field_filters:
        for field, value in field_filters.items():
            filter_parts.append(f'jsonPayload.{field}="{value}"')

    filter_string = " ".join(filter_parts)

    print(f"Fetching logs with filter: {filter_string}")
    entries = client.list_entries(filter_=filter_string, order_by=logging.DESCENDING)

    fetched_logs = []
    for entry in entries:
        if entry.payload:
            fetched_logs.append({
                "timestamp": entry.timestamp.isoformat(),
                "severity": entry.severity,
                "log_name": entry.log_name,
                "payload": entry.payload,
            })
    return fetched_logs

if __name__ == "__main__":
    # Example usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    print("Fetching recent logs for 'application_logs' from the last 30 minutes with component 'authentication_service'...")
    recent_auth_logs = fetch_recent_logs(
        log_name="application_logs",
        field_filters={"component": "authentication_service"},
        time_range_minutes=30
    )
    if recent_auth_logs:
        for log in recent_auth_logs:
            print(f"Log: {log['timestamp']} - {log['severity']} - {log['payload']}")
    else:
        print("No matching logs found.")

    print("\nFetching all recent 'correlated_application_logs' from the last 15 minutes...")
    all_correlated_logs = fetch_recent_logs(
        log_name="correlated_application_logs",
        time_range_minutes=15
    )
    if all_correlated_logs:
        for log in all_correlated_logs:
            print(f"Correlated Log: {log['timestamp']} - {log['severity']} - {log['payload']}")
    else:
        print("No correlated logs found.")
