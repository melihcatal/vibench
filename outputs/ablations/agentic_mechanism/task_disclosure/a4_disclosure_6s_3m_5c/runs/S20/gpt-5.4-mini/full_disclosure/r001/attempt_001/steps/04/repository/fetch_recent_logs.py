import os
from datetime import datetime, timedelta, timezone

import requests


def _isoformat_utc(dt):
    return dt.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')


def fetch_recent_logs(field_name, field_value, minutes=60, limit=100):
    api_key = os.environ.get('DATADOG_API_KEY')
    app_key = os.environ.get('DATADOG_APP_KEY')
    site = os.environ.get('DATADOG_SITE', 'datadoghq.com')
    if not api_key or not app_key:
        raise RuntimeError('DATADOG_API_KEY and DATADOG_APP_KEY are required')

    now = datetime.now(timezone.utc)
    start = now - timedelta(minutes=minutes)
    query = f'@{field_name}:{field_value}'
    payload = {
        'filter': {
            'from': _isoformat_utc(start),
            'to': _isoformat_utc(now),
            'query': query,
        },
        'page': {'limit': limit},
        'sort': 'desc',
    }
    response = requests.post(
        f'https://api.{site}/api/v2/logs/events/search',
        headers={
            'DD-API-KEY': api_key,
            'DD-APPLICATION-KEY': app_key,
            'Content-Type': 'application/json',
        },
        json=payload,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


if __name__ == '__main__':
    print(fetch_recent_logs('service', 'api'))
