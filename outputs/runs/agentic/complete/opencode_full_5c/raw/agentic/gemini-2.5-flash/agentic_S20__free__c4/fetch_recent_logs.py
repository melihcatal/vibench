import datetime
from typing import List, Dict, Any, Optional
from observability_client import ObservabilityClient


def fetch_recent_logs(
    log_name: str,
    time_range_minutes: int = 60,
    field_filters: Optional[Dict[str, str]] = None,
    project_id: Optional[str] = None,
    limit: int = 100,
) -> List[Dict[str, Any]]:
    """Retrieves recent log entries from Google Cloud Logging filtered by field values and time range.

    Args:
        log_name: The name of the log to query.
        time_range_minutes: The number of minutes back from now to search.
        field_filters: A dictionary of field names and their desired values to filter by.
                       e.g., {"jsonPayload.event": "user_login", "labels.environment": "production"}
        project_id: The GCP project ID. If None, it will be inferred from the client.
        limit: The maximum number of log entries to return.

    Returns:
        A list of dictionaries, where each dictionary represents a log entry.
    """
    client = ObservabilityClient().logging_client

    if project_id is None:
        project_id = client.project

    now = datetime.datetime.utcnow()
    time_ago = now - datetime.timedelta(minutes=time_range_minutes)

    # Base filter for log name and time range
    filter_string = (
        f'logName="projects/{project_id}/logs/{log_name}" AND '
        f'timestamp>="{time_ago.isoformat("T", "milliseconds")}Z"'
    )

    # Add additional field filters
    if field_filters:
        for field, value in field_filters.items():
            # Ensure values are properly quoted if they contain spaces or special characters
            if (
                " " in value
                or ":" in value
                or "/" in value
                or "-" in value
                or "." in value
            ):
                filter_string += f' AND {field}="{value}"'
            else:
                filter_string += f" AND {field}={value}"

    print(f"Fetching logs with filter: {filter_string}")

    entries = client.list_entries(
        filter_=filter_string,
        order_by=logging_v2.entries.ListLogEntriesRequest.OrderBy.TIMESTAMP_DESC,
        page_size=limit,
    )

    results = []
    for entry in entries:
        entry_dict = {
            "severity": entry.severity,
            "timestamp": entry.timestamp,
            "log_name": entry.log_name,
            "resource": entry.resource.to_dict(),
            "labels": dict(entry.labels),
        }
        if entry.text_payload:
            entry_dict["message"] = entry.text_payload
        elif entry.json_payload:
            entry_dict["json_payload"] = dict(entry.json_payload)
        else:
            entry_dict["message"] = "<no message content>"

        results.append(entry_dict)
        if len(results) >= limit:
            break

    return results


if __name__ == "__main__":
    # Example usage
    LOG_NAME_TO_FETCH = "my-structured-app-log"

    # Fetch logs with a specific event type in the JSON payload
    print("\n--- Fetching logs for user_login event ---")
    LOGIN_LOGS = fetch_recent_logs(
        LOG_NAME_TO_FETCH,
        time_range_minutes=120,
        field_filters={"jsonPayload.event": "user_login"},
    )

    if LOGIN_LOGS:
        print(f"Found {len(LOGIN_LOGS)} user login logs:")
        for log in LOGIN_LOGS:
            print(
                f"  [{log['timestamp']}] {log['severity']}: {log.get('json_payload', log.get('message'))} (Labels: {log['labels']})"
            )
    else:
        print("No user login logs found.")

    # Fetch logs with a specific severity and service label
    print("\n--- Fetching INFO logs for auth-service ---")
    AUTH_INFO_LOGS = fetch_recent_logs(
        LOG_NAME_TO_FETCH,
        time_range_minutes=120,
        field_filters={"severity": "INFO", "labels.service": "auth-service"},
    )

    if AUTH_INFO_LOGS:
        print(f"Found {len(AUTH_INFO_LOGS)} INFO logs for auth-service:")
        for log in AUTH_INFO_LOGS:
            print(
                f"  [{log['timestamp']}] {log['severity']}: {log.get('json_payload', log.get('message'))} (Labels: {log['labels']})"
            )
    else:
        print("No INFO logs found for auth-service.")
