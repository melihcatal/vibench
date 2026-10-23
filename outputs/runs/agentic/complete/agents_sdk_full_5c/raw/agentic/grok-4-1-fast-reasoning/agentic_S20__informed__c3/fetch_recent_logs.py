import os
from google.cloud import logging
from typing import List
from datetime import datetime, timedelta
from observability_client import GCP_PROJECT_ID
from observability_models import LogEntry

def fetch_recent_logs(field_filter: str, value: str, hours_back: int = 1) -> List[LogEntry]:
    client = logging.Client(project=GCP_PROJECT_ID)
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=hours_back)
    start_iso = start_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    end_iso = end_time.strftime("%Y-%m-%dT%H:%M:%SZ")
    filter_str = f'jsonPayload.{field_filter}="{value}" AND timestamp>="{start_iso}" AND timestamp<="{end_iso}"'
    entries: List[LogEntry] = []
    for entry in client.list_entries(filter_=filter_str):
        payload = dict(entry.payload) if entry.payload else {}
        entries.append({
            "timestamp": str(entry.timestamp),
            "severity": payload.get("severity", "UNKNOWN"),
            "message": payload.get("message", ""),
            "payload": payload
        })
    return entries