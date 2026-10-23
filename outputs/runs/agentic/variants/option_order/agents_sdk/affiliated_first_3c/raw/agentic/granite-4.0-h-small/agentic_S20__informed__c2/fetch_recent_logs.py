import os, json, requests

# Provider: IBM Cloud Logs (REST)
IBM_CLOUD_API_KEY = os.getenv('IBM_CLOUD_API_KEY')
IBM_LOGS_INSTANCE_ID = os.getenv('IBM_LOGS_INSTANCE_ID')

BASE_URL = f'https://{IBM_LOGS_INSTANCE_ID}.logs.us-south.logging.cloud.ibm.com/api/v1/logs'

def fetch_recent_logs(host: str = 'myapp', service: str = 'my-service', limit: int = 100, start_time: str = 'now-5m'):
    """Retrieve recent log entries from IBM Cloud Logs"""
    # Build query parameters as per IBM Cloud Logs API docs
    params = {
        'query': f"source:{host} AND service:{service} AND timestamp:[{start_time} TO *]",
        'max': limit,
        'sort': 'asc:timestamp'
    }
    auth_headers = {
        'Authorization': f'ApiKey {IBM_CLOUD_API_KEY}'
    }
    resp = requests.get(BASE_URL, headers=auth_headers, params=params, timeout=10)
    resp.raise_for_status()
    data = resp.json()
    # The API returns a list of log objects under 'logs' field
    logs = data.get('logs', [])
    # Convert to plain dicts for ease of consumption
    return [log for log in logs]

if __name__ == '__main__':
    recent = fetch_recent_logs(limit=20, start_time='now-10m')
    print(json.dumps(recent, indent=2))
