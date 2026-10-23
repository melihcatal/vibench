import os
from datetime import datetime, timedelta, timezone
from observability_client import ObservabilityClient


def fetch_recent_logs(user_id: str = "user-12345"):
    """
    Fetches recent logs from Google Cloud Logging filtered by a field value.
    """
    client = ObservabilityClient()
    logger_name = os.getenv("GCP_LOG_NAME", "my-structured-log")

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=30)

    start_str = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    end_str = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    filter_str = (
        f'logName="projects/{client.project_id}/logs/{logger_name}" '
        f'AND jsonPayload.user_id="{user_id}" '
        f'AND timestamp >= "{start_str}" '
        f'AND timestamp <= "{end_str}"'
    )

    print(f"Fetching logs with filter: {filter_str}")

    log_entries = client.query_logs(filter_str)

    results = []
    for entry in log_entries:
        results.append({"timestamp": entry.timestamp, "payload": entry.json_payload})
        print(entry)

    return results


if __name__ == "__main__":
    fetch_recent_logs()
