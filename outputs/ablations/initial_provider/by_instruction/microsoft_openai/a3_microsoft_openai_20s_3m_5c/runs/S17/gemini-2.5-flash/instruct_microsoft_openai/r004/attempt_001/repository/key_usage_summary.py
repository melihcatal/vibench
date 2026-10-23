import os
from datetime import datetime, timedelta
from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient, QueryTimeInterval

def summarize_key_usage(workspace_id: str, key_vault_name: str, time_range_hours: int = 24) -> dict:
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)

    query = f""
    AzureDiagnostics
    | where ResourceProvider == "MICROSOFT.KEYVAULT"
    | where Resource == "{key_vault_name}"
    | where Category == "AuditEvent"
    | summarize EventCount=count() by OperationName, KeyVaultName=Resource
    | order by EventCount desc
    ""

    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=time_range_hours)

    response = client.query_workspace(
        workspace_id,
        query,
        timespan=QueryTimeInterval(start_time, end_time)
    )

    summary = []
    for table in response.tables:
        for row in table.rows:
            summary.append({"operation_name": row[0], "key_vault_name": row[1], "event_count": row[2]})

    return {"key_usage_summary": summary}

