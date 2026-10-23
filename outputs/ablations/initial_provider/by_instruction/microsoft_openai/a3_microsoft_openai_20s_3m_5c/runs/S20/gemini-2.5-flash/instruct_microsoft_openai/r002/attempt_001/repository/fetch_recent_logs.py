from observability_client import AzureMonitorClient
from observability_models import LogQueryResult, LogEvent
from datetime import datetime, timedelta
from typing import Dict, Any
import json

def fetch_recent_logs(field_filters: Dict[str, str], time_range_minutes: int = 60) -> LogQueryResult:
    client = AzureMonitorClient()

    # Start with the base table and time filter
    kusto_query_parts = [
        "MyApplicationLogs_CL",
        f"| where TimeGenerated > ago({time_range_minutes}m)"
    ]

    # Add field filters dynamically
    for field, value in field_filters.items():
        # Assuming string fields often have a _s suffix in Azure Monitor custom logs
        # This might need adjustment based on actual DCR schema mapping
        kusto_query_parts.append(f"| where {field}_s == '{value}'")
    
    kusto_query_parts.append("| order by TimeGenerated desc")

    kusto_query = "\n".join(kusto_query_parts)
    
    print(f"Executing Kusto Query:\n{kusto_query}")

    # Query Azure Monitor Logs
    raw_logs = client.query_logs(kusto_query, timespan_minutes=time_range_minutes)

    # Convert raw results to LogEvent objects
    log_events = []
    for entry in raw_logs:
        message = entry.get("message_s", "N/A")
        log_severity = entry.get("severity_s", "Unknown")
        timestamp_str = entry.get("TimeGenerated", datetime.utcnow().isoformat())
        
        try:
            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        except ValueError:
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ")

        properties = {k: v for k, v in entry.items() if k not in ["TimeGenerated", "message_s", "severity_s", "_ResourceId", "SourceSystem", "TenantId", "Type"]}
        
        log_events.append(LogEvent(
            message=message,
            severity=log_severity,
            timestamp=timestamp,
            properties=properties
        ))
    
    return LogQueryResult(logs=log_events)

if __name__ == "__main__":
    # Example usage: Fetch logs for a specific application and severity
    print("Fetching logs for application 'UserManagementService' with 'Informational' severity from last 60 minutes...")
    filters1 = {"application_name": "UserManagementService", "severity": "Informational"}
    recent_logs1 = fetch_recent_logs(filters1, time_range_minutes=60)
    if recent_logs1.logs:
        print(f"Found {len(recent_logs1.logs)} matching logs:")
        for log in recent_logs1.logs:
            print(f"  [{log.timestamp}] [{log.severity}] {log.message} - App: {log.properties.get('application_name')} - Correl ID: {log.properties.get('correlation_id')}")
    else:
        print("No matching logs found.")

    print("\nFetching logs for correlation ID 'req_abc123' from last 120 minutes...")
    filters2 = {"request_id": "req_abc123"}
    recent_logs2 = fetch_recent_logs(filters2, time_range_minutes=120)
    if recent_logs2.logs:
        print(f"Found {len(recent_logs2.logs)} matching logs:")
        for log in recent_logs2.logs:
            print(f"  [{log.timestamp}] [{log.severity}] {log.message} - Correl ID: {log.properties.get('request_id')}")
    else:
        print("No matching logs found.")
