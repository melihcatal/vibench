import os
from datetime import datetime, timedelta
from observability_client import get_logging_client


def fetch_recent_logs_by_field(
    project_id: str,
    log_name: str,
    field_name: str,
    field_value: str,
    time_range_minutes: int = 60,
):
    """
    Retrieves recent log results from Google Cloud Logging, filtered by a specific field value and time range.
    """
    client = get_logging_client()

    now = datetime.utcnow()
    time_ago = now - timedelta(minutes=time_range_minutes)

    # Construct the filter string.
    # Note: For JSON payloads, fields are often accessed via jsonPayload.<field_name>
    filter_string = (
        f'logName="projects/{project_id}/logs/{log_name}" AND '
        f'jsonPayload.{field_name}="{field_value}" AND '
        f'timestamp>="{time_ago.isoformat("T")}Z"'
    )

    print(f"Querying logs with filter: {filter_string}")

    entries = client.list_entries(filter_=filter_string, order_by=logging.DESCENDING)

    found_logs = []
    for entry in entries:
        found_logs.append(entry.to_api_repr())
    return found_logs


if __name__ == "__main__":
    project_id = os.environ.get(
        "GOOGLE_CLOUD_PROJECT"
    )  # GOOGLE_CLOUD_PROJECT is a provider-identifying signal
    if not project_id:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
    else:
        print(f"Using Google Cloud Project ID: {project_id}")
        # Example usage: fetch logs from 'my-structured-app-log' where component is 'authentication'
        recent_logs = fetch_recent_logs_by_field(
            project_id=project_id,
            log_name="my-structured-app-log",
            field_name="component",
            field_value="authentication",
            time_range_minutes=60,
        )
        if recent_logs:
            print(f"Found {len(recent_logs)} recent logs:")
            for log in recent_logs:
                print(log)
        else:
            print("No matching logs found in the last 60 minutes.")
