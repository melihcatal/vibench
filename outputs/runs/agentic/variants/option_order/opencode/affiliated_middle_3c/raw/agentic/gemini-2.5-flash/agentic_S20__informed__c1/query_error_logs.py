import os
from datetime import datetime, timedelta
from observability_client import get_logging_client
from observability_models import parse_log_entry

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")  # Ensure this env var is set


def query_error_logs(time_range_minutes: int = 60):
    client = get_logging_client()

    now = datetime.utcnow()
    time_filter = now - timedelta(minutes=time_range_minutes)
    time_filter_str = time_filter.isoformat("T") + "Z"

    # Filter for ERROR severity and logs within the time range
    # Google Cloud Logging query language: https://cloud.google.com/logging/docs/view/logging-query-language
    filter_str = f'severity=(ERROR OR CRITICAL OR ALERT OR EMERGENCY) AND timestamp >= "{time_filter_str}"'

    print(f"Querying error logs with filter: {filter_str}")

    entries = client.list_entries(filter_=filter_str, order_by="timestamp desc")

    found_errors = []
    for entry in entries:
        parsed_entry = parse_log_entry(entry.to_api_repr())
        found_errors.append(parsed_entry)

    return found_errors


if __name__ == "__main__":
    errors = query_error_logs(time_range_minutes=120)  # Query errors from last 2 hours
    if errors:
        print(f"Found {len(errors)} error logs:")
        for error in errors:
            print(
                f"  [{error['timestamp']}] {error['severity']}: {error['message']} (Component: {error['component']})"
            )
    else:
        print("No error logs found in the specified time range.")
