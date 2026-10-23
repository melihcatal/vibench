import os, requests, datetime

# IBM Cloud Logs - Query API (REST)
BASE_URL = 'https://api.us-south.logs.cloud.ibm.com/v1'
INSTANCE_ID = os.getenv('IBM_LOGS_INSTANCE_ID')
API_KEY = os.getenv('IBM_CLOUD_API_KEY')


def query_error_logs(start_time: str, end_time: str = None) -> list:
    """Query recent ERROR-level logs for a time window.

    Args:
        start_time: ISO-8601 datetime string (inclusive). Example: '2025-08-15T00:00:00Z'
        end_time: Optional ISO-8601 datetime string (exclusive). Defaults to now.

    Returns:
        List of log entries (as dicts) that match ERROR severity.
    """
    if not end_time:
        end_time = datetime.datetime.utcnow().isoformat() + 'Z'
    query = f'severity:ERROR AND timestamp:[{start_time} TO {end_time}]'
    url = f"{BASE_URL}/instances/{INSTANCE_ID}/query"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'apikey {API_KEY}'
    }
    payload = {'query': query}
    response = requests.post(url, json=payload, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()['logs']
