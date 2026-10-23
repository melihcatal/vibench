import os
from datetime import datetime, timedelta, timezone
from observability_client import get_logging_client


def query_recent_errors(minutes: int = 60):
    """
    Queries for ERROR severity log entries in the last N minutes
    from Google Cloud Logging.
    """
    client = get_logging_client()

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)

    # Format timestamps in RFC3339 UTC "Z" format.
    start_time_str = start_time.isoformat("T") + "Z"
    end_time_str = end_time.isoformat("T") + "Z"

    # https://cloud.google.com/logging/docs/view/logging-query-language
    filter_str = (
        f'severity="ERROR" '
        f'timestamp>="{start_time_str}" AND timestamp<="{end_time_str}"'
    )

    print(f"Querying for error logs with filter: {filter_str}")

    entries = client.list_entries(filter_=filter_str, order_by=client.DESCENDING)

    error_logs = []
    for entry in entries:
        log_payload = {
            "timestamp": entry.timestamp.isoformat(),
            "severity": entry.severity,
            "payload": entry.payload,
        }
        error_logs.append(log_payload)
        print(log_payload)

    return error_logs


if __name__ == "__main__":
    if os.environ.get("GCP_PROJECT_ID"):
        query_recent_errors()
    else:
        print("GCP_PROJECT_ID environment variable not set. Skipping example run.")
