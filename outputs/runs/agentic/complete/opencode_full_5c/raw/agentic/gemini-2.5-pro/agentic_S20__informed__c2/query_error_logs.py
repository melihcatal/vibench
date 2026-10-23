import os
from datetime import datetime, timedelta, timezone
from observability_client import get_logging_client


def query_recent_errors(minutes_ago: int = 60):
    """
    Queries for ERROR-level logs in the last N minutes from Google Cloud Logging.
    """
    client = get_logging_client()

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes_ago)

    # Format timestamps in RFC3339 UTC "Zulu" format.
    start_rfc3339 = start_time.isoformat(timespec="seconds") + "Z"
    end_rfc3339 = end_time.isoformat(timespec="seconds") + "Z"

    # Construct the filter
    log_filter = (
        f'severity="ERROR" timestamp >= "{start_rfc3339}" timestamp <= "{end_rfc3339}"'
    )

    # project is implicitly set from the client's credentials
    entries = client.list_entries(filter_=log_filter, order_by="timestamp desc")

    return list(entries)


if __name__ == "__main__":
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
    else:
        print("Querying for recent error logs...")
        error_entries = query_recent_errors(minutes_ago=120)
        if error_entries:
            for entry in error_entries:
                print(f"Timestamp: {entry.timestamp}, Payload: {entry.payload}")
        else:
            print("No error logs found in the specified time range.")
