import requests
from typing import List, Dict, Any
from datetime import datetime

# Datadog Events API Configuration
DATADOG_API_KEY = os.getenv("DATADOG_API_KEY", "your-datadog-api-key")
DATADOG_APP_KEY = os.getenv("DATADOG_APP_KEY", "your-datadog-app-key")
DATADOG_EVENTS_URL = "https://api.datadoghq.com/api/v1/events"


def summarize_audit_events(events: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Summarize federated login audit events and send to Datadog."""
    summary = {
        "total_logins": len(events),
        "providers": {},
        "event_types": {},
        "time_range": {
            "start": min(e["timestamp"] for e in events),
            "end": max(e["timestamp"] for e in events),
        },
    }

    for event in events:
        provider = event["provider"]
        event_type = event["event_type"]

        summary["providers"][provider] = summary["providers"].get(provider, 0) + 1
        summary["event_types"][event_type] = (
            summary["event_types"].get(event_type, 0) + 1
        )

    _send_to_datadog(summary)
    return summary


def _send_to_datadog(summary: Dict[str, Any]) -> None:
    """Send summary to Datadog Events API."""
    headers = {
        "Content-Type": "application/json",
        "DD-API-KEY": DATADOG_API_KEY,
        "DD-APPLICATION-KEY": DATADOG_APP_KEY,
    }
    payload = {
        "title": "Federated Login Audit Summary",
        "text": f"Total logins: {summary['total_logins']}",
        "tags": [f"provider:{k}" for k in summary["providers"].keys()],
        "date_happened": int(datetime.now().timestamp()),
        "aggregation_key": "federated_login_audit",
    }
    requests.post(DATADOG_EVENTS_URL, headers=headers, json=payload)
