from datetime import datetime, timedelta, timezone

from observability_client import build_client, load_config


def fetch_recent_logs(field_name: str, field_value: str, hours: int = 6) -> list[dict]:
    cfg = load_config()
    client = build_client()
    start = datetime.now(timezone.utc) - timedelta(hours=hours)
    query = (
        f'resource.type="global" AND logName="projects/{cfg.project_id}/logs/{cfg.log_name}" '
        f'AND jsonPayload.{field_name}="{field_value}" AND timestamp>="{start.isoformat()}"'
    )
    entries = client.list_entries(filter_=query, page_size=100)
    return [
        {
            "timestamp": e.timestamp.isoformat() if e.timestamp else None,
            "payload": dict(e.payload) if hasattr(e.payload, "items") else e.payload,
            "severity": e.severity,
        }
        for e in entries
    ]
