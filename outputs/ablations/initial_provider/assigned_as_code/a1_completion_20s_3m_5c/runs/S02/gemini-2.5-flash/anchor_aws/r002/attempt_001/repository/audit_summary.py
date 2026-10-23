import os
from typing import Dict, Any, List
from datetime import datetime, timedelta
import requests

from identity_models import AuditRecord

# Datadog API configuration
DATADOG_API_KEY = os.environ.get("DATADOG_API_KEY", "YOUR_DATADOG_API_KEY")
DATADOG_APP_KEY = os.environ.get("DATADOG_APP_KEY", "YOUR_DATADOG_APP_KEY")
DATADOG_API_URL = os.environ.get("DATADOG_API_URL", "https://api.datadoghq.com/api/v1/events")

def summarize_audit_events(event_type: str, time_range_minutes: int = 60) -> Dict[str, Any]:
    headers = {
        "Content-Type": "application/json",
        "DD-API-KEY": DATADOG_API_KEY,
        "DD-APPLICATION-KEY": DATADOG_APP_KEY,
    }

    end_time = int(datetime.now().timestamp())
    start_time = int((datetime.now() - timedelta(minutes=time_range_minutes)).timestamp())

    # Datadog events API to search for specific events
    # This is a simplified example; a real integration might use logs API or metrics
    # to get more granular summaries.
    params = {
        "start": start_time,
        "end": end_time,
        "query": f"tags:event_type:{event_type} sources:federated-login",
        "priority": "normal",
        "unaggregated": "true"
    }

    try:
        response = requests.get(DATADOG_API_URL, headers=headers, params=params)
        response.raise_for_status()
        events_data = response.json()
        
        # Process events_data to create a summary
        summary = {
            "event_type": event_type,
            "total_events": len(events_data.get("events", [])),
            "time_range_minutes": time_range_minutes,
            "summary_details": events_data # For simplicity, returning raw events for now
        }
        return summary
    except requests.exceptions.RequestException as e:
        print(f"Error fetching Datadog events: {e}")
        return {"error": str(e)}

