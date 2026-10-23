from datetime import datetime, timezone
from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient

from observability_client import get_query_client


def fetch_recent_logs(config=None, field_name=None, field_value=None, start_time=None, end_time=None):
    config = config or {}
    client = get_query_client(config)
    query = f""" 
    traces
    | where timestamp >= datetime('{start_time}') and timestamp <= datetime('{end_time}')
    """
    if field_name and field_value:
        query += f" | where {field_name} == '{field_value}'"
    response = client.query_workspace(config['workspace_id'], query)
    return response.tables[0].rows