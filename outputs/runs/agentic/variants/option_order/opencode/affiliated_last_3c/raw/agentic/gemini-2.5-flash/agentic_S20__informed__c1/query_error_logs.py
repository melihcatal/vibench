import os
import datetime
from observability_client import get_logging_client
from observability_models import LogErrorQuery


def query_error_logs(query: LogErrorQuery):
    client = get_logging_client()

    # Calculate the start time for the query
    now = datetime.datetime.utcnow()
    start_time = now - datetime.timedelta(seconds=query.time_range_seconds)

    # Construct the filter string
    # Note: Cloud Logging uses 'timestamp' for the log entry's timestamp
    filter_string = (
        f"severity={query.severity} AND "
        f'timestamp>="{start_time.isoformat()}"Z AND '
        f'resource.labels.project_id="{query.project_id}"'
    )

    print(f"Querying logs with filter: {filter_string}")

    entries = client.list_entries(filter_=filter_string, project_ids=[query.project_id])

    error_logs = []
    for entry in entries:
        error_logs.append(entry)

    print(
        f"Found {len(error_logs)} error logs in the last {query.time_range_seconds} seconds:"
    )
    for log in error_logs:
        print(f"  [{log.severity}] {log.timestamp}: {log.payload}")
    return error_logs


if __name__ == "__main__":
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        error_query = LogErrorQuery(
            project_id=project_id, severity="ERROR", time_range_seconds=3600
        )
        query_error_logs(error_query)
