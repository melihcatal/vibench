import os
from datetime import datetime, timedelta, timezone
from observability_client import ObservabilityClient
from observability_models import LogQuery, LogQueryResult


def fetch_recent_logs(
    field_filters: dict,
    time_range_minutes: int = 60,
    log_name: str = "application-logs",
) -> LogQueryResult:
    """Retrieves recent log results from Google Cloud Logging filtered by field values and time range."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = ObservabilityClient(project_id, log_name=log_name)

    now = datetime.now(timezone.utc)
    n_minutes_ago = now - timedelta(minutes=time_range_minutes)

    filter_parts = [
        f'timestamp>="{n_minutes_ago.isoformat(timespec="seconds")}"',
        f'timestamp<="{now.isoformat(timespec="seconds")}"',
        f'logName="projects/{project_id}/logs/{log_name}"',
    ]

    for field, value in field_filters.items():
        # Handle different types of fields (e.g., textPayload, jsonPayload fields)
        if field == "message":
            filter_parts.append(f'textPayload:"{value}"')
        elif (
            field.startswith("jsonPayload.")
            or field.startswith("labels.")
            or field.startswith("resource.")
        ):
            filter_parts.append(f'{field}="{value}"')
        else:
            filter_parts.append(
                f'{field}="{value}"'
            )  # Default for other top-level fields

    filter_string = " AND ".join(filter_parts)

    log_query = LogQuery(filter_string=filter_string)
    entries = client.list_log_entries(
        log_query.filter_string, log_query.order_by, log_query.page_size
    )

    result = LogQueryResult(entries)
    print(
        f"Fetched recent logs with filters {field_filters} in the last {time_range_minutes} minutes."
    )
    return result


if __name__ == "__main__":
    # Example usage:
    # Assuming logs with jsonPayload.event_type = "user_login" exist
    filters = {"jsonPayload.event_type": "user_login", "severity": "INFO"}
    recent_logs = fetch_recent_logs(filters, time_range_minutes=60)
    if recent_logs.entries:
        print("Found recent logs:")
        print(recent_logs.to_json())
    else:
        print("No recent logs found matching the filters.")
