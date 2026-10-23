from datetime import datetime, timezone
from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient

from observability_client import get_query_client


def query_error_logs(config=None, severity='Error', start_time=None, end_time=None):
    config = config or {}
    client = get_query_client(config)
    query = f""" 
    traces
    | where severity == '{severity}'
    | where timestamp >= datetime('{start_time}') and timestamp <= datetime('{end_time}')
    | project timestamp, message, severity
    """
    response = client.query_workspace(config['workspace_id'], query)
    return response.tables[0].rows