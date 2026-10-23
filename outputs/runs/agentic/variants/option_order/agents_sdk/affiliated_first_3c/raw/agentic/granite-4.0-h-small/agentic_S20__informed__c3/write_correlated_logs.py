import requests, os, uuid, datetime

# IBM Cloud Logs - REST API
BASE_URL = 'https://api.us-south.logs.cloud.ibm.com/v1'
INSTANCE_ID = os.getenv('IBM_LOGS_INSTANCE_ID')
API_KEY = os.getenv('IBM_CLOUD_API_KEY')


def write_correlated_logs(message: str, correlation_id: str, level: str = 'INFO') -> dict:
    """Write application log events with a shared correlation (request) ID.

    Args:
        message: Text payload of the log.
        correlation_id: Identifier linking related log entries.
        level: Severity (INFO, ERROR, ...).

    Returns:
        Deserialized JSON response from the logging service.
    """
    if isinstance(message, str):
        message = {'message': message}
    log_entry = {
        'timestamp': datetime.datetime.utcnow().isoformat() + 'Z',
        'correlation_id': correlation_id,
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
