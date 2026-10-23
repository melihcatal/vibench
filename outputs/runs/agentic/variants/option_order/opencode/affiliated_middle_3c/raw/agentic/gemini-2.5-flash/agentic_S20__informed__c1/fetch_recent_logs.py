import os
from datetime import datetime, timedelta
from observability_client import get_logging_client
from observability_models import parse_log_entry

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")  # Ensure this env var is set
LOG_NAME = "my-application-log"


def fetch_recent_logs(
    time_range_minutes: int = 60,
    component: str = None,
    severity: str = None,
    correlation_id: str = None,
):
    client = get_logging_client()

    now = datetime.utcnow()
    time_filter = now - timedelta(minutes=time_range_minutes)
    time_filter_str = time_filter.isoformat("T") + "Z"

    filters = [
        f'logName="projects/{PROJECT_ID}/logs/{LOG_NAME}"',
        f'timestamp >= "{time_filter_str}"',
    ]

    if component:
        filters.append(f'jsonPayload.component="{component}"')
    if severity:
        filters.append(f'severity="{severity.upper()}"')
    if correlation_id:
        filters.append(f'jsonPayload.correlation_id="{correlation_id}"')

    filter_str = " AND ".join(filters)

    print(f"Fetching recent logs with filter: {filter_str}")

    entries = client.list_entries(filter_=filter_str, order_by="timestamp desc")

    recent_logs = []
    for entry in entries:
        parsed_entry = parse_log_entry(entry.to_api_repr())
        recent_logs.append(parsed_entry)

    return recent_logs


if __name__ == "__main__":
    # Example 1: Fetch all recent logs
    all_recent_logs = fetch_recent_logs(time_range_minutes=30)
    print(f"Found {len(all_recent_logs)} recent logs (all types):")
    for log in all_recent_logs:
        print(f"  [{log['timestamp']}] {log['severity']}: {log['message']}")

    print("\n" + "-" * 50 + "\n")

    # Example 2: Fetch recent logs for a specific component and severity
    component_logs = fetch_recent_logs(
        time_range_minutes=60, component="authentication", severity="INFO"
    )
    print(f"Found {len(component_logs)} 'authentication' INFO logs:")
    for log in component_logs:
        print(f"  [{log['timestamp']}] {log['severity']}: {log['message']}")
