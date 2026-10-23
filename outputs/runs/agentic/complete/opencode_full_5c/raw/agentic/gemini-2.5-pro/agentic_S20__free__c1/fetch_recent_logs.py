from datetime import datetime, timedelta, timezone
from observability_client import get_logging_client, get_project_id
from observability_models import QueryResult


def fetch_recent_logs(
    log_name: str, user_id: str, hours_ago: int = 1
) -> list[QueryResult]:
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
        f'AND jsonPayload.user_id="{user_id}" '
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
    # This assumes logs for user 'user-12345' have been written
    recent_logs = fetch_recent_logs(
        "my-structured-log", user_id="user-12345", hours_ago=24
    )
    if recent_logs:
        print(f"Found {len(recent_logs)} logs for user 'user-12345':")
        for log in recent_logs:
            print(log)
    else:
        print("No recent logs found for the specified user and time range.")
