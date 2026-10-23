from datetime import datetime, timezone
from typing import Any, Dict, Optional
from google.cloud import logging_v2
from observability_client import build_logging_client, load_observability_config
from observability_models import LogQueryRequest, LogQueryResponse, LogRecord


def fetch_recent_logs(field_name: str, field_value: Any, hours: int = 6, limit: int = 100) -> LogQueryResponse:
    config = load_observability_config()
    client = build_logging_client(config)
    end_time = datetime.now(timezone.utc)
    start_time = end_time - __import__("datetime").timedelta(hours=hours)
    request = LogQueryRequest(start_time=start_time, end_time=end_time, field_filters={field_name: field_value}, limit=limit)
    value_text = str(request.field_filters[field_name])
    query = f'timestamp>="{request.start_time.isoformat()}" timestamp<="{request.end_time.isoformat()}" jsonPayload.{field_name}="{value_text}"'
    entries = list(client.list_entries(filter_=query, page_size=request.limit))
    records = []
    for entry in entries[: request.limit]:
        payload = dict(entry.payload) if isinstance(entry.payload, dict) else {"payload": entry.payload}
        records.append(LogRecord(timestamp=entry.timestamp, severity=str(entry.severity), message=str(payload.get("message", entry.payload)), payload=payload))
    return LogQueryResponse(records=records)
