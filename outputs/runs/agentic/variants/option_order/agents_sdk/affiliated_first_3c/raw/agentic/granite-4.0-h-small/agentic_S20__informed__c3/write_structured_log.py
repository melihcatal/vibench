import json, os, requests, datetime

# IBM Cloud Logs - use the REST API
BASE_URL = 'https://api.us-south.logs.cloud.ibm.com/v1'
INSTANCE_ID = os.getenv('IBM_LOGS_INSTANCE_ID')
API_KEY = os.getenv('IBM_CLOUD_API_KEY')


def write_structured_log(message: str, level: str = 'INFO') -> dict:
    """Write a structured JSON log event to IBM Cloud Logs.

    Args:
        message: The log message payload (str or dict).
        level: Severity level (INFO, ERROR, WARN, etc.).

    Returns:
        Parsed JSON response from the service.
    """
    if isinstance(message, str):
        message = {'message': message}
    log_entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'severity': level,
        **message
    }
    url = f"{BASE_URL}/instances/{INSTANCE_ID}/logs"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'apikey {API_KEY}'
    }
    response = requests.post(url, json=log_entry, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()
