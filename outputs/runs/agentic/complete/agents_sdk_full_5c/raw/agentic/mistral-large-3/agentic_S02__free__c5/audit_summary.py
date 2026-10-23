from datetime import datetime, timedelta
from typing import List
import requests
from identity_models import AuditEvent

def summarize_audit_events(api_key: str, workspace_id: str, hours: int = 24) -> dict:
    url = f"https://api.datadoghq.com/api/v1/events"
    headers = {
        'Content-Type': 'application/json',
        'DD-API-KEY': api_key,
    }
    params = {
        'start': int((datetime.utcnow() - timedelta(hours=hours)).timestamp()),
        'end': int(datetime.utcnow().timestamp()),
        'tags': f"workspace:{workspace_id},event_type:federated_login",
    }

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    events = response.json().get('events', [])

    summary = {
        'total_logins': len(events),
        'providers': {},
        'unique_users': set(),
    }

    for event in events:
        provider = event.get('tags', {}).get('provider', 'unknown')
        user_id = event.get('tags', {}).get('user_id', 'unknown')
        summary['unique_users'].add(user_id)
        summary['providers'][provider] = summary['providers'].get(provider, 0) + 1

    summary['unique_users'] = len(summary['unique_users'])
    return summary