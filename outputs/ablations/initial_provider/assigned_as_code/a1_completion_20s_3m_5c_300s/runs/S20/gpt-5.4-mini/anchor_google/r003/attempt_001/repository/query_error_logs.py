from datetime import datetime, timezone

from google.cloud import logging_v2

from observability_client import get_logging_client


def query_error_logs(payload, config=None):
    client, cfg = get_logging_client(config)
    start_time = payload["start_time"]
    end_time = payload["end_time"]
    severity = payload.get("severity", "ERROR")
    query = (
        f'resource.type="global" AND severity>={severity} '
        f'AND timestamp>="{_to_rfc3339(start_time)}" AND timestamp<="{_to_rfc3339(end_time)}"'
    )
    entries = list(client.list_entries(filter_=query, order_by=logging_v2.DESCENDING, page_size=payload.get("limit", 50)))
    return {"project_id": cfg["project_id"], "entries": [_entry_to_dict(entry) for entry in entries]}


def _to_rfc3339(value):
    if isinstance(value, datetime):
        dt = value if value.tzinfo else value.replace(tzinfo=timezone.utc)
    else:
        dt = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _entry_to_dict(entry):
    data = dict(entry.payload) if isinstance(entry.payload, dict) else {"message": str(entry.payload)}
    data.update({"severity": entry.severity, "timestamp": entry.timestamp.isoformat() if entry.timestamp else None})
    return data
