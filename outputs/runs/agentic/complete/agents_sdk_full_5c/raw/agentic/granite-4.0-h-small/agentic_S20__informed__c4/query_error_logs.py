import os
from typing import List, Dict
from observability_client import get_datadog_client

def query_error_logs(severity: str = 'error', start: int = None, end: int = None) -> List[Dict]:
    """Query Datadog for recent error log entries within a time range.

    Returns a list of log records (each a dict) matching the severity and time window.
    """
    client = get_datadog_client()
    query = f"dd.error:true severity:{severity}"
    if start or end:
        query += f" starttime:{start} endtime:{end}"
    print('Executing Datadog query:', query)
    response = client.logs.query(query=query, index='default')
    if response.ok:
        result = response.json().get('logs', [])
        return result
    else:
        print('Error querying logs:', response.text)
        return []
