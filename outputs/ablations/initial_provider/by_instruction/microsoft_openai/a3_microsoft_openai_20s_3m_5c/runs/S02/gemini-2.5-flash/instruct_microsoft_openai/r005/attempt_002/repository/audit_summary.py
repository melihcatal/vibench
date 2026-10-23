
import os
from azure.monitor.query import LogsQueryClient, QueryTimeRange
from azure.identity import DefaultAzureCredential
import datetime

def summarize_audit_events(workspace_id: str, time_range_hours: int = 24) -> str:
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)

    # Kusto Query Language (KQL) to query Azure Active Directory sign-in logs
    # Note: Requires Azure AD logs to be sent to Log Analytics workspace
    query = f"SigninLogs | where TimeGenerated > ago({time_range_hours}h) | summarize EventCount = count() by ResultType, Identity"

    try:
        response = client.query_workspace(
            workspace_id=workspace_id,
            query=query,
            timespan=QueryTimeRange(datetime.timedelta(hours=time_range_hours))
        )

        summary = ["Federated Login Audit Summary:"]
        
        if response.tables:
            for row in response.tables[0].rows:
                summary.append(f"  Result: {row[0]}, Identity: {row[1]}, Count: {row[2]}")
        else:
            summary.append("  No audit events found within the specified time range.")

        print("\n".join(summary))
        return "\n".join(summary)

    except Exception as e:
        print(f"Error querying Azure Monitor Logs: {e}")
        return f"Error summarizing audit events: {e}"

if __name__ == '__main__':
    # Example usage: Set your Azure Log Analytics Workspace ID
    # os.environ['AZURE_LOG_ANALYTICS_WORKSPACE_ID'] = 'YOUR_LOG_ANALYTICS_WORKSPACE_ID'
    
    workspace_id = os.environ.get('AZURE_LOG_ANALYTICS_WORKSPACE_ID', 'YOUR_LOG_ANALYTICS_WORKSPACE_ID')
    
    if workspace_id != 'YOUR_LOG_ANALYTICS_WORKSPACE_ID':
        summarize_audit_events(workspace_id)
    else:
        print("Please set the AZURE_LOG_ANALYTICS_WORKSPACE_ID environment variable to run this example.")

