from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient


def key_usage_summary(payload, config=None):
    config = config or {}
    workspace_id = config['workspace_id']
    query = payload.get('query', 'AzureDiagnostics | summarize count() by OperationName')
    with DefaultAzureCredential() as credential:
        client = LogsQueryClient(credential)
        result = client.query_workspace(workspace_id, query, timespan=payload.get('timespan'))
    return {'tables': [table.rows for table in result.tables], 'status': result.status}
