import os
from typing import List, Dict
from observability_client import get_datadog_client

def fetch_recent_logs(field_filters: List[str] = None, start: int = None, end: int = None) -> List[Dict]:
    """Retrieve recent logs that match optional field filters and a time window.

    field_filters: e.g., ['service:my_service', 'env:prod'] formatted as query strings
    start, end: Unix timestamps (seconds) for the query window
    Returns matching log records.
    """
    client = get_datadog_client()
    query = 'scrape:true'
    if field_filters:
        query += ' ' + ' '.join(field_filters)
    if start or end:
        query += f" starttime:{start} endtime:{end}"
    print('Fetching recent logs with query:', query)
    response = client.logs.query(query=query, index='default')
    if response.ok:
        return response.json().get('logs', [])
    else:
        print('Failed to fetch recent logs:', response.text)
        return []
