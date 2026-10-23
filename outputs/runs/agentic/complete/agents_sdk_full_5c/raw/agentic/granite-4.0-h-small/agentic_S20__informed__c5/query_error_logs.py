import os, datetime, requests

BASE_URL = 'https://logging.googleapis.com/v2'
API_KEY = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

def query_error_logs(start_time: datetime.datetime, end_time: datetime.datetime, severity: str = 'ERROR') -> list:
    """Queries recent error log entries from Google Cloud Logging.

    Args:
        start_time: Inclusive lower bound timestamp.
        end_time: Exclusive upper bound timestamp.
        severity: Log severity filter (default 'ERROR').

    Returns:
        List of log entry objects matching the criteria.
    """
    url = f'{BASE_URL}/entries:list'
    start_iso = start_time.isoformat() + 'Z'
    end_iso = end_time.isoformat() + 'Z'
    query = {
        'resourceNames': ['projects/your-project-id'],
        'filter': f'severity={severity} AND timestamp>="{start_iso}" AND timestamp<"{end_iso}"'
    }
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }
    resp = requests.post(url, headers=headers, json=query)
    resp.raise_for_status()
    data = resp.json()
    return data.get('entries', [])
