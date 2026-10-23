import json, os, requests

# Provider: Datadog Logs API
DD_API_KEY = os.getenv('DD_API_KEY')
DD_APP_KEY = os.getenv('DD_APP_KEY')

BASE_URL = 'https://http-intake.logs.datadoghq.com/v1/input'

def write_structured_log(message: str, host: str = 'myapp', service: str = 'my-service', tags: list[str] = None):
    """Write a structured JSON log event to Datadog"""
    payload = {
        'ddsource': host,
        'ddtags': tags,
        'message': message,
        'hostname': host,
        'service': service,
        'ddtags': ','.join(tags) if tags else None
    }
    headers = {
        'Content-Type': 'application/json',
        'DD-API-KEY': DD_API_KEY,
        'DD-APPLICATION-KEY': DD_APP_KEY
    }
    response = requests.post(BASE_URL, headers=headers, data=json.dumps(payload), timeout=10)
    response.raise_for_status()
    return response.json()

if __name__ == '__main__':
    write_structured_log('Test log from Python')
