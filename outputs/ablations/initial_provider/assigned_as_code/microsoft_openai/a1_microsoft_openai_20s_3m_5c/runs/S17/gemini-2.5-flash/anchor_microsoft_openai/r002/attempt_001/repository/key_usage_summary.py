from azure.monitor.query import LogsQueryClient, QueryTimeRange
from azure.identity import DefaultAzureCredential
from datetime import datetime, timedelta
import os

def get_key_usage_summary(tenant_id: str, workspace_id: str, days: int = 7) -> str:
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)

    # Kusto query to summarize Key Vault operations
    query = f"""
    AzureDiagnostics
    | where ResourceProvider == "MICROSOFT.KEYVAULT"
    | where Category == "AuditEvent"
    | where OperationName contains "Key"
    | summarize count() by OperationName, ResultType
    | order by count_ desc
    """

    # Define the time range for the query
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=days)
    time_range = QueryTimeRange(start_time, end_time)

    response = client.query_workspace(
        workspace_id=workspace_id,
        query=query,
        timespan=time_range
    )

    summary = "Key Usage Summary (last {} days):\n".format(days)
    for table in response.tables: # type: ignore
        for row in table.rows:
            summary += f"- Operation: {row[0]}, Result: {row[1]}, Count: {row[2]}\n"

    return summary


# Example usage (requires AZURE_TENANT_ID and AZURE_MONITOR_WORKSPACE_ID env vars to be set)
# if __name__ == "__main__":
#     tenant_id = os.environ.get("AZURE_TENANT_ID")
#     workspace_id = os.environ.get("AZURE_MONITOR_WORKSPACE_ID")
#     if tenant_id and workspace_id:
#         summary = get_key_usage_summary(tenant_id, workspace_id)
#         print(summary)
#     else:
#         print("Please set AZURE_TENANT_ID and AZURE_MONITOR_WORKSPACE_ID environment variables.")
