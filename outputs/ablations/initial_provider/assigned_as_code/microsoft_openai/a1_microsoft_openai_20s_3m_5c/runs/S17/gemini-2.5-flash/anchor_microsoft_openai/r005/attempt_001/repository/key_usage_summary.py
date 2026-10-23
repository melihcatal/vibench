import os
from datetime import datetime, timedelta
from azure.identity import DefaultAzureCredential
from azure.monitor.query import LogsQueryClient, QueryTimeInterval

def summarize_key_usage(workspace_id: str, key_vault_name: str, time_range_hours: int = 24) -> dict:
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)

    # Kusto Query Language (KQL) to query Azure Key Vault diagnostics logs
    query = f"""
    AzureDiagnostics
    | where ResourceProvider == "MICROSOFT.KEYVAULT"
    | where ResourceType == "VAULTS"
    | where Resource =~ "{key_vault_name}"
    | where Category == "AuditEvent"
    | project TimeGenerated, OperationName, ResultType, identity_claim_objectId_g, id_g, OperationVersion, correlationId_g
    | summarize EventCount=count() by OperationName, ResultType
    | order by EventCount desc
    """

    # Define the time range for the query
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(hours=time_range_hours)
    time_interval = QueryTimeInterval(start_time, end_time)

    response = client.query_workspace(
        workspace_id=workspace_id,
        query=query,
        timespan=time_interval
    )

    summary = {"key_vault_name": key_vault_name, "time_range_hours": time_range_hours, "usage_summary": []}
    if response.tables:
        for row in response.tables[0].rows:
            summary["usage_summary"].append({
                "operation_name": row[0], # OperationName
                "result_type": row[1], # ResultType
                "event_count": row[2]  # EventCount
            })

    return summary

# Example usage (requires AZURE_TENANT_ID, AZURE_CLIENT_ID, AZURE_CLIENT_SECRET, and AZURE_MONITOR_WORKSPACE_ID env vars)
# Also, ensure Azure Key Vault diagnostic settings are configured to send logs to the Log Analytics Workspace.
# print(summarize_key_usage(os.environ["AZURE_MONITOR_WORKSPACE_ID"], "your_key_vault_name"))
