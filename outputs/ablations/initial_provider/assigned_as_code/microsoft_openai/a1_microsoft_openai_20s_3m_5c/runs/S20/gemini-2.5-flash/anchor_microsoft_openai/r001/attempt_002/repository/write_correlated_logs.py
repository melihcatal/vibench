import os
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List

from observability_client import AzureMonitorClient
from observability_models import LogEntry

def write_correlated_logs(log_events: List[Dict[str, Any]], correlation_id: Optional[str] = None, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    config = config or {}
    correlation_id = correlation_id or str(uuid.uuid4())

    client = AzureMonitorClient(
        workspace_id=config.get("AZURE_MONITOR_WORKSPACE_ID"),
        rule_id=config.get("AZURE_MONITOR_RULE_ID"),
        stream_name=config.get("AZURE_MONITOR_STREAM_NAME"),
        logging_endpoint=config.get("AZURE_MONITOR_LOGGING_ENDPOINT"),
        query_endpoint=config.get("AZURE_MONITOR_QUERY_ENDPOINT")
    )

    log_entries = []
    for event_data in log_events:
        message = event_data.get("message", "")
        severity = event_data.get("severity", "INFO")
        timestamp = event_data.get("timestamp")
        if isinstance(timestamp, (int, float)): # Assume Unix timestamp if int or float
            timestamp = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        elif isinstance(timestamp, str):
            try:
                timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            except ValueError:
                timestamp = datetime.now(timezone.utc)
        else:
            timestamp = datetime.now(timezone.utc)

        properties = {k: v for k, v in event_data.items() if k not in ["message", "severity", "timestamp"]}
        properties["correlationId"] = correlation_id
        log_entries.append(LogEntry(message=message, severity=severity, timestamp=timestamp, **properties))

    return client.ingest_log_entries(log_entries)
