import datetime
from typing import List, Dict, Any
from observability_client import ObservabilityClient


def query_error_logs(
    log_name: str,
    min_severity: str = "ERROR",
    time_range_minutes: int = 60,
    project_id: str = None,
) -> List[Dict[str, Any]]:
    """Queries recent error log entries from Google Cloud Logging filtered by severity and time range.

    Args:
        log_name: The name of the log to query (e.g., "my-app-log").
        min_severity: The minimum severity level to filter by (e.g., "ERROR", "WARNING").
        time_range_minutes: The number of minutes back from now to search.
        project_id: The GCP project ID. If None, it will be inferred from the client.

    Returns:
        A list of dictionaries, where each dictionary represents a log entry.
    """
    client = ObservabilityClient().logging_client

    if project_id is None:
        project_id = client.project

    now = datetime.datetime.utcnow()
    time_ago = now - datetime.timedelta(minutes=time_range_minutes)

    # Construct the filter string
    # https://cloud.google.com/logging/docs/view/advanced-queries
    filter_string = (
        f'logName="projects/{project_id}/logs/{log_name}" AND '
        f'severity>="{min_severity.upper()}" AND '
        f'timestamp>="{time_ago.isoformat("T", "milliseconds")}Z"'
    )

    print(f"Querying logs with filter: {filter_string}")

    entries = client.list_entries(
        filter_=filter_string,
        order_by=logging_v2.entries.ListLogEntriesRequest.OrderBy.TIMESTAMP_DESC,
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
    return results


if __name__ == "__main__":
    # Example usage
    LOG_NAME_TO_QUERY = "my-correlated-app-log"
    ERROR_LOGS = query_error_logs(
        LOG_NAME_TO_QUERY, min_severity="ERROR", time_range_minutes=120
    )

    if ERROR_LOGS:
        print(
            f"Found {len(ERROR_LOGS)} error logs in the last 120 minutes from {LOG_NAME_TO_QUERY}:"
        )
        for log in ERROR_LOGS:
            print(
                f"  [{log['timestamp']}] {log['severity']}: {log.get('message', log.get('json_payload'))} (Labels: {log['labels']})"
            )
    else:
        print(f"No error logs found in the last 120 minutes from {LOG_NAME_TO_QUERY}.")

    # Example with a specific project_id if needed
    # import os
    # PROJECT_ID = os.environ.get("GCP_PROJECT_ID")
    # if PROJECT_ID:
    #     CRITICAL_LOGS = query_error_logs(LOG_NAME_TO_QUERY, min_severity="CRITICAL", time_range_minutes=30, project_id=PROJECT_ID)
    #     print(f"Found {len(CRITICAL_LOGS)} critical logs.")
