import os
from datetime import datetime, timedelta
from google.cloud import logging
from observability_client import ObservabilityClient
from observability_models import LogQueryResult


def fetch_recent_logs(
    log_name: str, field_filters: dict = None, time_range_minutes: int = 60
) -> list[LogQueryResult]:
    """Retrieves recent log results filtered by field values and time range from Google Cloud Logging."""
    client = ObservabilityClient()
    logging_client = client.logging_client

    now = datetime.utcnow()
    start_time = now - timedelta(minutes=time_range_minutes)

    filter_parts = [
        f'resource.type="global"',
        f'logName="projects/{client.project_id}/logs/{log_name}"',
        f'timestamp>="{start_time.isoformat()}Z"',
    ]

    if field_filters:
        for field, value in field_filters.items():
            # Example: jsonPayload.user_id="user-123", textPayload:"Starting"
            filter_parts.append(f'{field}="{value}"')

    filter_string = " AND ".join(filter_parts)

    print(f"Fetching logs with filter: {filter_string}")
    entries = logging_client.list_entries(
        filter_=filter_string, order_by="timestamp desc"
    )

    results = []
    for entry in entries:
        results.append(LogQueryResult(entry.to_dict()))
    return results


if __name__ == "__main__":
    # Example usage: Ensure GOOGLE_CLOUD_PROJECT environment variable is set
    log_name = "my-structured-app-log"  # Or any other log name you've written to

    # Example 1: Fetch all recent logs for a given log_name
    all_recent_logs = fetch_recent_logs(log_name, time_range_minutes=60)
    if all_recent_logs:
        print(f"\nFound {len(all_recent_logs)} recent logs (all):")
        for log in all_recent_logs:
            print(f"  [{log.timestamp}] {log.severity}: {log.message}")

    # Example 2: Fetch logs with a specific field value in jsonPayload
    field_filters = {"jsonPayload.user_id": "user-123"}
    filtered_logs = fetch_recent_logs(
        log_name, field_filters=field_filters, time_range_minutes=60
    )

    if filtered_logs:
        print(
            f'\nFound {len(filtered_logs)} recent logs (filtered by user_id="user-123"):'
        )
        for log in filtered_logs:
            print(
                f"  [{log.timestamp}] {log.severity}: {log.message} (Payload: {log.json_payload})"
            )
    else:
        print("No logs found matching the filter.")
