import os, json, requests

# Environment variables for IBM Cloud Logs
BASE_URL = 'https://api.us-south.logs.cloud.ibm.com/v1'
INSTANCE_ID = os.getenv('IBM_LOGS_INSTANCE_ID')
API_KEY = os.getenv('IBM_CLOUD_API_KEY')


def _log(url, payload, method='POST'):
    """Internal helper to call the IBM Cloud Logs REST API."""
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'apikey {API_KEY}'
    }
    resp = requests.request(method, url, json=payload, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()


def write_structured_log(message: str, level: str = 'INFO') -> dict:
    """Write a structured JSON log entry to IBM Cloud Logs."""
    if isinstance(message, str):
        message = {'message': message}
    log_entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'severity': level,
        **message
    }
    return _log(f'{BASE_URL}/instances/{INSTANCE_ID}/logs', log_entry)


def query_logs(query: str) -> list:
    """Execute a KQL query and return the results."""
    url = f'{BASE_URL}/instances/{INSTANCE_ID}/query'
    payload = {'query': query}
    return _log(url, payload, method='POST')


def search_logs(query: str, limit: int = 100) -> list:
    """Search logs by a user‑provided query expression."""
    url = f'{BASE_URL}/instances/{INSTANCE_ID}/search'
    payload = {'query': query, 'limit': limit}
    return _log(url, payload, method='POST')
