from datetime import datetime, timedelta, timezone

from google.cloud.logging_v2.entries import LogEntry

from observability_client import build_client, load_config


def query_error_logs(hours: int = 24, severity: str = "ERROR") -> list[dict]:
    cfg = load_config()
    client = build_client()
    start = datetime.now(timezone.utc) - timedelta(hours=hours)
    query = (
        f'resource.type="global" AND logName="projects/{cfg.project_id}/logs/{cfg.log_name}" '
        f'AND severity>={severity} AND timestamp>="{start.isoformat()}"'
    )
    entries = client.list_entries(filter_=query, page_size=50)
    results = []
    for entry in entries:
        if isinstance(entry, LogEntry):
            results.append(
                {
                    "timestamp": entry.timestamp.isoformat()
                    if entry.timestamp
                    else None,
                    "payload": dict(entry.payload)
                    if hasattr(entry.payload, "items")
                    else entry.payload,
                    "severity": entry.severity,
                }
            )
    return results
