from azure.monitor.query import LogsQueryClient
from azure.identity import DefaultAzureCredential
from datetime import timedelta, datetime
import os

def summarize_secret_rotation_status(secret_name: str, timespan_days: int = 30) -> dict:
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)
    workspace_id = os.environ.get("AZURE_LOG_ANALYTICS_WORKSPACE_ID")
    if not workspace_id:
        raise ValueError("AZURE_LOG_ANALYTICS_WORKSPACE_ID environment variable not set.")

    query_time = timedelta(days=timespan_days)

    # Kusto Query Language (KQL) to find Key Vault secret rotation related events
    # Operations related to secret versions often indicate rotation or updates
    query = f"""
    AzureDiagnostics
    | where ResourceProvider == "MICROSOFT.KEYVAULT"
    | where ResourceType == "VAULTS"
    | where OperationName has "Secret"
    | where SecretName_s == '{secret_name}'
    | where TimeGenerated > ago({timespan_days}d)
    | summarize count() by OperationName, ResultType
    | order by OperationName asc
    """

    response = client.query_workspace(workspace_id, query, timespan=query_time)

    summary = {
        "secret_name": secret_name,
        "timespan_days": timespan_days,
        "rotation_events": []
    }

    for row in response.tables[0].rows:
        summary["rotation_events"].append({
            "operation_name": row[0],
            "result_type": row[1],
            "count": row[2]
        })

    return summary
