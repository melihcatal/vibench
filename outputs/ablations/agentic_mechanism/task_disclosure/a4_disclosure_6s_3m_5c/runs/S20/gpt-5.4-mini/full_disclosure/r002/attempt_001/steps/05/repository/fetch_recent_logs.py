import os
from datetime import datetime, timedelta, timezone

import requests


def fetch_recent_logs(field_name, field_value, minutes_back=60, limit=100):
    api_key = os.getenv("SIGNALFIRE_API_KEY")
    workspace_id = os.getenv("SIGNALFIRE_WORKSPACE_ID")
    if not api_key or not workspace_id:
        raise EnvironmentError("SIGNALFIRE_API_KEY and SIGNALFIRE_WORKSPACE_ID are required")

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes_back)
    url = f"https://api.signalfx.com/v2/logs/query"
    payload = {
        "workspaceId": workspace_id,
        "limit": limit,
        "timeRange": {
            "start": start_time.isoformat(),
            "end": end_time.isoformat(),
        },
        "filters": [
            {
                "field": field_name,
                "operator": "eq",
                "value": field_value,
            }
        ],
        "sort": {"field": "timestamp", "direction": "desc"},
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }
    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    return response.json()
