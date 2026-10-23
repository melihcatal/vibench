from google.cloud import logging
import os
from datetime import datetime, timedelta, timezone

def fetch_recent_logs(log_name: str, days_back: int = 1, field_filters: dict = None, limit: int = 10):
    """
    Retrieves recent log results from Google Cloud Logging filtered by field values and time range.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = logging.Client(project=project_id)

    now = datetime.now(timezone.utc)
    n_days_ago = now - timedelta(days=days_back)

    base_filter = f'logName="projects/{project_id}/logs/{log_name}" AND timestamp>="{n_days_ago.isoformat(timespec="seconds")}"'

    if field_filters:
        filter_parts = [base_filter]
        for field, value in field_filters.items():
            # For simplicity, assuming string comparison. More complex filters might need different handling.
            if isinstance(value, str):
                filter_parts.append(f'{field}="{value}'')
            else:
                filter_parts.append(f'{field}={value}'')
        full_filter = " AND ".join(filter_parts)
    else:
        full_filter = base_filter

    print(f"Fetching logs with filter: {full_filter}")

    entries = client.list_entries(
        filter_=full_filter,
        order_by=logging.DESCENDING,
        page_size=limit
    )

    fetched_logs = []
    for i, entry in enumerate(entries):
        if i >= limit:
            break
        entry_dict = entry.to_api_repr()
        fetched_logs.append(entry_dict)
        print(f"Found Log [{entry.severity}]: {entry.timestamp} {entry.payload}")

    return fetched_logs

if __name__ == "__main__":
    # Example usage (requires GOOGLE_CLOUD_PROJECT env var and auth)
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    print("\n--- Fetching recent INFO logs for user-123 ---")
    recent_info_logs = fetch_recent_logs(
        "my-app-logs",
        days_back=0,
        field_filters={
            "jsonPayload.user_id": "user-123",
            "severity": "INFO"
        },
        limit=5
    )
    print(f"\nTotal recent info logs found: {len(recent_info_logs)}")

    print("\n--- Fetching recent WARN logs ---")
    recent_warn_logs = fetch_recent_logs(
        "my-app-logs",
        days_back=0,
        field_filters={
            "severity": "WARNING"
        },
        limit=3
    )
    print(f"\nTotal recent warn logs found: {len(recent_warn_logs)}")
