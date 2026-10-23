import os
from google.cloud import logging_v2
from google.cloud.logging_v2.proto import log_entry_pb2
from datetime import datetime, timedelta


def summarize_login_audit_events(
    project_id: str,
    time_window_hours: int = 24,
    event_type_filter: str = None,
) -> dict:
    client = logging_v2.Client(project=project_id)

    # Calculate time range for the query
    now = datetime.utcnow()
    start_time = now - timedelta(hours=time_window_hours)
    start_time_str = start_time.isoformat("T") + "Z"
    now_str = now.isoformat("T") + "Z"

    # Construct the filter
    filters = [
        f'resource.type="cloud_run_revision" OR resource.type="gce_instance"',
        f'timestamp>="{start_time_str}"',
        f'timestamp<="{now_str}"',
        'jsonPayload.event_type="federated_login"',
    ]
    if event_type_filter:
        filters.append(f'jsonPayload.details.event_type="{event_type_filter}"')
    
    # Add a filter for the specific log name, assuming logs are written to 'federated_login_audit'
    filters.append('logName="projects/{}/logs/federated_login_audit"'.format(project_id))

    full_filter = " AND ".join(filters)

    entries = client.list_entries(filter_=full_filter, order_by=logging_v2.SortOrder.NEWEST)

    summary = {
        "total_events": 0,
        "event_types": {},
        "users": {},
        "time_window_hours": time_window_hours,
    }

    for entry in entries:
        summary["total_events"] += 1
        payload = entry.json_payload
        event_type = payload.get("event_type", "unknown")
        user_id = payload.get("user_id", "anonymous")

        summary["event_types"][event_type] = summary["event_types"].get(event_type, 0) + 1
        summary["users"][user_id] = summary["users"].get(user_id, 0) + 1

    return summary
