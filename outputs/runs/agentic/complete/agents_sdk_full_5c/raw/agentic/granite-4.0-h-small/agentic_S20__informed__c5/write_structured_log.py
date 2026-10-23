import os, json, requests

BASE_URL = 'https://logs.googleapis.com/v2'
API_KEY = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

def write_structured_log(resource: str, severity: str, message: dict) -> dict:
    """Writes a structured JSON log event to Google Cloud Logging.

    Args:
        resource: The monitored resource identifier (e.g., 'global').
        severity: Log severity level (e.g., 'ERROR').
        message: A dictionary containing log fields.

    Returns:
        The parsed response JSON from the API.
    """
    log_entry = {
        'severity': severity,
        'jsonPayload': message,
        'resource': {'type': resource}
    }
    url = f'{BASE_URL}/entries:write'
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    payload = {'logEntries': [log_entry]}
    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()
    return resp.json()
