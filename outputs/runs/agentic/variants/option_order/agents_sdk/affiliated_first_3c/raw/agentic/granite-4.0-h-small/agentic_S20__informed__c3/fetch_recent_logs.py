import os, requests, datetime

# IBM Cloud Logs - Search API (REST)
BASE_URL = 'https://api.us-south.logs.cloud.ibm.com/v1'
INSTANCE_ID = os.getenv('IBM_LOGS_INSTANCE_ID')
API_KEY = os.getenv('IBM_CLOUD_API_KEY')


def fetch_recent_logs(field: str, value: str, start_time: str, end_time: str = None) -> list:
    """Retrieve recent logs filtered by a field=value pair and a time window.

    Args:
        field: Log field name (e.g., 'hostname', 'service', 'user').
        value: Exact value to match.
        start_time: ISO-8601 datetime string (inclusive).
        end_time: Optional ISO-8601 datetime string (exclusive). Defaults to now.

    Returns:
        A list of matching log entries (each a dict).
    """
    if not end_time:
        end_time = datetime.datetime.utcnow().isoformat() + 'Z'
    url = f"{BASE_URL}/instances/{INSTANCE_ID}/search"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'apikey {API_KEY}'
    }
    payload = {
        'query': f'{field}:{value} AND timestamp:[{start_time} TO {end_time}]',
        'limit': 100  # adjust as needed
    }
    response = requests.post(url, json=payload, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json().get('hits', [])
