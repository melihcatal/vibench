from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient

from security_client import load_security_config


def key_usage_summary(payload, config=None):
    config = load_security_config(config)
    with DefaultAzureCredential() as credential:
        client = LogsQueryClient(credential)
        query = payload.get('query') or "AzureDiagnostics | summarize count() by OperationName"
        return {'query': query, 'workspace_id': config.get('workspace_id'), 'provider': 'azure-monitor'}
