from typing import List, Dict, Any
import datetime
import os
from google.cloud import logging_v2

# Google Cloud Logging Configuration
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "your-gcp-project-id")
LOG_NAME = "federated-login-audit"

def summarize_audit_events(filter_query: str = None) -> List[Dict[str, Any]]:
    """Summarize federated-login audit events from Google Cloud Logging."""
    client = logging_v2.Client(project=GCP_PROJECT_ID)
    filter_str = f"logName=\"projects/{GCP_PROJECT_ID}/logs/{LOG_NAME}\""
    if filter_query:
        filter_str += f" AND {filter_query}"

    entries = client.list_entries(
        filter_=filter_str,
        max_results=1000,
        order_by=logging_v2 DESCENDING,
    )
    
    summary = []
    for entry in entries:
        payload = entry.payload
        summary.append({
            "timestamp": entry.timestamp.isoformat(),
            "user_id": payload.get("user_id"),
            "provider": payload.get("provider"),
            "event_type": payload.get("event_type"),
            "ip_address": payload.get("ip_address"),
            "user_agent": payload.get("user_agent"),
            "metadata": payload.get("metadata", {}),
        })
    
    return summary