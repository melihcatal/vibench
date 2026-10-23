import os
from datetime import datetime, timedelta
from typing import List
import requests
from identity_models import LoginAuditRecord


def summarize_audit_events(api_key: str, days: int = 7) -> dict:
    url = "https://api.datadoghq.com/api/v1/events"
    headers = {
        "Content-Type": "application/json",
        "DD-API-KEY": api_key,
    }
    
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)
    
    params = {
        "start": int(start_time.timestamp()),
        "end": int(end_time.timestamp()),
        "priority": "normal",
        "tags": "service:federated-login",
    }
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    
    events = response.json().get("events", [])
    summary = {
        "total_logins": len(events),
        "providers": {},
        "time_range": {
            "start": start_time.isoformat(),
            "end": end_time.isoformat(),
        },
    }
    
    for event in events:
        provider = event.get("tags", {}).get("provider", "unknown")
        summary["providers"][provider] = summary["providers"].get(provider, 0) + 1
    
    return summary