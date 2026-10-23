from datetime import datetime, timedelta, timezone
from observability_client import get_logging_client, get_project_id
from observability_models import QueryResult


def query_error_logs(log_name: str, hours_ago: int = 1) -> list[QueryResult]:
    client = get_logging_client()
    project_id = get_project_id()
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    resource_names = [f"projects/{project_id}"]

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(hours=hours_ago)

    time_format = "%Y-%m-%dT%H:%M:%S.%fZ"

    filter_str = (
        f'logName="projects/{project_id}/logs/{log_name}" '
        f'AND severity="ERROR" '
        f'AND timestamp >= "{start_time.strftime(time_format)}" '
        f'AND timestamp <= "{end_time.strftime(time_format)}"'
    )

    entries = client.list_log_entries(resource_names=resource_names, filter_=filter_str)

    results = []
    for entry in entries:
        result: QueryResult = {
            "timestamp": entry.timestamp.isoformat(),
            "severity": entry.severity,
            "message": entry.json_payload.get("message", ""),
            "payload": dict(entry.json_payload),
        }
        results.append(result)
    return results


if __name__ == "__main__":
    # This assumes error logs have been written to 'my-structured-log'
    errors = query_error_logs("my-structured-log", hours_ago=24)
    if errors:
        print(f"Found {len(errors)} error logs:")
        for error in errors:
            print(error)
    else:
        print("No error logs found in the specified time range.")
