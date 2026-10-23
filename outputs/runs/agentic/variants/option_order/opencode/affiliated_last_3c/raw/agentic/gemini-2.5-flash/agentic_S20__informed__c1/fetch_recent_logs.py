import os
import datetime
from observability_client import get_logging_client
from observability_models import LogQuery


def fetch_recent_logs(query: LogQuery):
    client = get_logging_client()

    # Calculate the start time for the query
    now = datetime.datetime.utcnow()
    start_time = now - datetime.timedelta(seconds=query.time_range_seconds)

    # Construct the filter string
    filter_string = (
        f"{query.filter_string} AND "
        f'timestamp>="{start_time.isoformat()}"Z AND '
        f'resource.labels.project_id="{query.project_id}"'
    )

    print(f"Fetching logs with filter: {filter_string}")

    entries = client.list_entries(filter_=filter_string, project_ids=[query.project_id])

    recent_logs = []
    for entry in entries:
        recent_logs.append(entry)

    print(
        f"Found {len(recent_logs)} recent logs in the last {query.time_range_seconds} seconds:"
    )
    for log in recent_logs:
        print(f"  [{log.severity}] {log.timestamp}: {log.payload}")
    return recent_logs


if __name__ == "__main__":
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        # Example: Fetch logs with a specific user_id in jsonPayload
        recent_log_query = LogQuery(
            project_id=project_id,
            filter_string='jsonPayload.user_id="user-123"',
            time_range_seconds=3600,
        )
        fetch_recent_logs(recent_log_query)
