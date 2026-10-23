from datetime import datetime, timezone
from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient, LogsQueryOptions


def summarize_error_logs(config=None):
    config = config or {}
    with DefaultAzureCredential() as credential:
        client = LogsQueryClient(credential)
        query = 'YourLogTableName | where Severity == "Error" and TimeGenerated > ago(1d) | summarize count() by bin(TimeGenerated, 1h)'
        options = LogsQueryOptions(start_time=datetime.now(timezone.utc) - timedelta(days=1), end_time=datetime.now(timezone.utc))
        response = client.query_workspace(config['workspace_id'], query, options)
    return response.tables[0].rows if response.tables else []