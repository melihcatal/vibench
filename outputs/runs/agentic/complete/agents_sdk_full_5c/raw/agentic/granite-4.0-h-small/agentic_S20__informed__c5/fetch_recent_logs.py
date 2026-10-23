import os, datetime, requests

BASE_URL = 'https://logging.googleapis.com/v2'
API_KEY = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')

def fetch_recent_logs(start_time: datetime.datetime, end_time: datetime.datetime, field_filter: dict) -> list:
    """Fetches recent log entries filtered by field values and time range.

    Args:
        start_time: Inclusive start of the time window.
        end_time: Exclusive end of the time window.
        field_filter: Dict of field name => value to apply as a filter.

    Returns:
        List of matching log entry dictionaries.
    """
    url = f'{BASE_URL}/entries:list'
    start_iso = start_time.isoformat() + 'Z'
    end_iso = end_time.isoformat() + 'Z'
    filter_expr = 'timestamp>="{}" AND timestamp<"{}"'.format(start_iso, end_iso)
    for key, value in field_filter.items():
        filter_expr += f' AND jsonPayload.{key}="{value}"'
    query = {
        'resourceNames': ['projects/your-project-id'],
        'filter': filter_expr
    }
    headers = {
        'Authorization': f'Bearer {API_KEY}'
    }
    response = requests.post(url, headers=headers, json=query)
    response.raise_for_status()
    data = response.json()
    return data.get('entries', [])
