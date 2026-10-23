import os, json, requests

BASE_URL = 'https://logs.googleapis.com/v2'
API_KEY = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

def write_correlated_logs(resource: str, correlation_id: str, logs: list) -> dict:
    """Writes multiple structured log events that share a correlation identifier.

    Args:
        resource: Monitored resource type.
        correlation_id: Shared request/trace ID to associate logs.
        logs: List of log payload dictionaries.

    Returns:
        Parsed JSON response from Google Cloud Logging API.
    """
    log_entries = []
    for payload in logs:
        entry = {
            'severity': payload.get('severity', 'INFO'),
            'jsonPayload': payload,
            'resource': {'type': resource},
            'labels': {'correlation_id': correlation_id}
        }
        log_entries.append(entry)

    url = f'{BASE_URL}/entries:write'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {'logEntries': log_entries}
    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()
    return resp.json()
