import os
from datetime import datetime, timedelta, timezone
from observability_client import ObservabilityClient


def query_error_logs():
    """
    Queries for recent error logs in Google Cloud Logging.
    """
    client = ObservabilityClient()
    logger_name = os.getenv("GCP_LOG_NAME", "my-structured-log")

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=1)

    # Format for Google Cloud Logging filter
    start_str = start_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    end_str = end_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    filter_str = (
        f'logName="projects/{client.project_id}/logs/{logger_name}" '
        f'AND severity="ERROR" '
        f'AND timestamp >= "{start_str}" '
        f'AND timestamp <= "{end_str}"'
    )

    print(f"Querying for error logs with filter: {filter_str}")

    log_entries = client.query_logs(filter_str)

    results = []
    for entry in log_entries:
        results.append(
            {
                "timestamp": entry.timestamp,
                "severity": entry.severity,
                "payload": entry.json_payload,
            }
        )
        print(entry)

    return results


if __name__ == "__main__":
    query_error_logs()
