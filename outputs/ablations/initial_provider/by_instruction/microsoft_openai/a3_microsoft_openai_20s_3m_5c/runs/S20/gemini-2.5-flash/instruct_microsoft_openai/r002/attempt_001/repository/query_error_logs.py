from observability_client import AzureMonitorClient
from observability_models import LogQueryResult, LogEvent
from datetime import datetime, timedelta
from typing import List
import json

def query_error_logs(severity: str = "Error", time_range_minutes: int = 60) -> LogQueryResult:
    client = AzureMonitorClient()
    
    # Kusto Query Language (KQL) for Azure Monitor
    # Assuming the custom logs are ingested into a table named 'MyApplicationLogs_CL'
    # The actual table name depends on the 'Custom Log Table Name' chosen during DCR creation
    # For this example, let's assume the stream 'Custom-MyApplicationLogs' maps to 'MyApplicationLogs_CL'
    kusto_query = f"""
    MyApplicationLogs_CL
    | where severity_s == '{severity}'
    | order by TimeGenerated desc
    """

    # Query Azure Monitor Logs
    raw_logs = client.query_logs(kusto_query, timespan_minutes=time_range_minutes)

    # Convert raw results to LogEvent objects
    log_events = []
    for entry in raw_logs:
        # Assuming 'TimeGenerated' is the timestamp field from Azure Monitor
        # and 'message_s', 'severity_s' are the message and severity fields
        # Other fields are part of properties
        message = entry.get("message_s", "N/A")
        log_severity = entry.get("severity_s", "Unknown")
        timestamp_str = entry.get("TimeGenerated", datetime.utcnow().isoformat())
        
        try:
            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00')) # Handle Z for UTC
        except ValueError:
            timestamp = datetime.strptime(timestamp_str, "%Y-%m-%dT%H:%M:%S.%fZ") # Fallback for older formats

        properties = {k: v for k, v in entry.items() if k not in ["TimeGenerated", "message_s", "severity_s", "_ResourceId", "SourceSystem", "TenantId", "Type"]}
        
        log_events.append(LogEvent(
            message=message,
            severity=log_severity,
            timestamp=timestamp,
            properties=properties
        ))
    
    return LogQueryResult(logs=log_events)

if __name__ == "__main__":
    # Example usage: Query critical errors from the last 120 minutes
    print("Querying critical error logs from the last 120 minutes...")
    critical_errors = query_error_logs(severity="Critical", time_range_minutes=120)
    if critical_errors.logs:
        print(f"Found {len(critical_errors.logs)} critical error logs:")
        for log in critical_errors.logs:
            print(f"  [{log.timestamp}] [{log.severity}] {log.message} - Properties: {log.properties}")
    else:
        print("No critical error logs found.")

    print("\nQuerying any errors from the last 60 minutes...")
    all_errors = query_error_logs(severity="Error", time_range_minutes=60)
    if all_errors.logs:
        print(f"Found {len(all_errors.logs)} error logs:")
        for log in all_errors.logs:
            print(f"  [{log.timestamp}] [{log.severity}] {log.message} - Properties: {log.properties}")
    else:
        print("No error logs found.")
