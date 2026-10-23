from azure.monitor.query import LogsQueryClient, QueryTimeRange
from azure.identity import DefaultAzureCredential
from datetime import datetime, timedelta
from typing import List, Dict, Any
from security_models import KeyUsageEvent

def summarize_key_usage(tenant_id: str, workspace_id: str, time_range_days: int = 7) -> List[KeyUsageEvent]:
    """Summarizes key usage and crypto events from Azure Monitor Logs."""
    credential = DefaultAzureCredential()
    client = LogsQueryClient(credential)

    # Define the time range for the query
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(days=time_range_days)

    # Kusto Query Language (KQL) to query Azure Key Vault diagnostics logs
    # This query assumes Key Vault diagnostics are enabled and sent to a Log Analytics Workspace.
    # The logs are typically found in the AzureDiagnostics table.
    # For Key Vault, the category would be 'AuditEvent'.
    kusto_query = f"""
    AzureDiagnostics
    | where ResourceProvider == "MICROSOFT.KEYVAULT"
    | where Category == "AuditEvent"
    | where TimeGenerated between (datetime('{start_time.isoformat()}Z')..datetime('{end_time.isoformat()}Z'))
    | project TimeGenerated, OperationName, resource_id, identity_s, properties_s
    | order by TimeGenerated desc
    """

    response = client.query_workspace(
        workspace_id=workspace_id,
        query=kusto_query,
        timespan=QueryTimeRange(start_time=start_time, end_time=end_time)
    )

    key_usage_events: List[KeyUsageEvent] = []
    if response.tables:
        for row in response.tables[0].rows:
            # Example parsing - adjust based on actual log structure
            # AzureDiagnostics rows are often dynamic, so direct indexing might need care.
            # Here we assume a certain order based on the 'project' statement.
            # You might need to inspect actual log output for robust parsing.
            
            # Example: OperationName will tell us encrypt/decrypt/sign/verify
            operation_name = row[1] if len(row) > 1 else "UnknownOperation"
            resource_id = row[2] if len(row) > 2 else "UnknownKey"
            timestamp = row[0].isoformat() if len(row) > 0 else datetime.utcnow().isoformat()
            
            # Extract key_id from resource_id or properties_s if available
            key_id = "N/A"
            if resource_id and "/keys/" in resource_id:
                key_id_parts = resource_id.split('/keys/')
                if len(key_id_parts) > 1:
                    key_id = key_id_parts[1].split('/')[0] # Get the key name
            
            # properties_s often contains JSON string of detailed properties
            # For a real implementation, you'd parse properties_s if it's a JSON string
            details: Dict[str, Any] = {"raw_log": row[3]} # For demonstration, just keep raw properties

            event_type = "unknown"
            if "Encrypt" in operation_name: event_type = "encrypt"
            elif "Decrypt" in operation_name: event_type = "decrypt"
            elif "Sign" in operation_name: event_type = "sign"
            elif "Verify" in operation_name: event_type = "verify"
            elif "Key" in operation_name: event_type = "key_management"
            
            key_usage_events.append(
                KeyUsageEvent(
                    event_type=event_type,
                    key_id=key_id,
                    timestamp=timestamp,
                    details=details
                )
            )
    return key_usage_events
