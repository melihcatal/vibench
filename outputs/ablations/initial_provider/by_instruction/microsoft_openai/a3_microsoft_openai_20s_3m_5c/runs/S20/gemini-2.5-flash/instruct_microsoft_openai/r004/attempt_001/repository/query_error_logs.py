from datetime import datetime, timedelta
from typing import List
from observability_client import ObservabilityClient
from observability_models import LogEntry, LogQueryResult
from azure.monitor.query import LogsQueryStatus

def query_error_logs(time_range_minutes: int = 60) -> LogQueryResult:
    client = ObservabilityClient()
    logs_query_client = client.get_logs_query_client()
    workspace_id = client.get_log_analytics_workspace_id()

    if not logs_query_client or not workspace_id:
        print("Azure Log Analytics client not configured. Cannot query error logs.")
        return LogQueryResult([], datetime.utcnow(), 0)

    # Kusto Query Language (KQL) for Azure Log Analytics
    # This query searches for 'traces' table (from Application Insights) with severity 'ERROR' or 'CRITICAL'
    # and also a custom 'LogEntry' table if it was ingested directly (which isn't via OpenTelemetry default)
    # For OpenTelemetry traces, severity is often mapped to 'SeverityLevel' in 'traces' table
    query = f"""
traces
| where SeverityLevel == '4' or SeverityLevel == '3' // 3 for error, 4 for critical in Application Insights SDK
| where TimeGenerated > ago({time_range_minutes}m)
| project TimeGenerated, Message=AppMessage, Severity=SeverityLevel, CustomDimensions
| order by TimeGenerated desc
"""

    # For custom logs ingested via Data Collector API or custom tables, the query would look like:
    # query = f"""
    # MyCustomLogs_CL
    # | where severity_s == 'ERROR' or severity_s == 'CRITICAL'
    # | where TimeGenerated > ago({time_range_minutes}m)
    # | project TimeGenerated, message_s, severity_s, properties_s
    # | order by TimeGenerated desc
    # """

    try:
        response = logs_query_client.query_workspace(workspace_id, query, timespan=None)

        if response.status == LogsQueryStatus.SUCCESS:
            error_entries: List[LogEntry] = []
            for table in response.tables: # Assuming only one table in response for this query
                for row in table.rows:
                    # Map KQL results to LogEntry model
                    time_generated = row[table.columns.index("TimeGenerated")]
                    message = row[table.columns.index("Message")]
                    severity_level = row[table.columns.index("Severity")] # '3' or '4'
                    custom_dimensions_str = row[table.columns.index("CustomDimensions")]

                    severity_map = {'3': 'ERROR', '4': 'CRITICAL'}
                    severity = severity_map.get(str(severity_level), 'UNKNOWN')

                    properties = {}
                    if custom_dimensions_str:
                        try:
                            properties = json.loads(custom_dimensions_str)
                        except json.JSONDecodeError:
                            pass # Ignore if not valid JSON

                    error_entries.append(LogEntry(
                        message=message,
                        severity=severity,
                        timestamp=time_generated,
                        properties=properties
                    ))
            print(f"Found {len(error_entries)} error logs in the last {time_range_minutes} minutes.")
            return LogQueryResult(error_entries, datetime.utcnow(), len(error_entries))
        else:
            print(f"Log query failed with status: {response.status}. Error: {response.partial_error}")
            return LogQueryResult([], datetime.utcnow(), 0)
    except Exception as e:
        print(f"An error occurred during log query: {e}")
        return LogQueryResult([], datetime.utcnow(), 0)

if __name__ == "__main__":
    # Example usage:
    result = query_error_logs(time_range_minutes=30)
    for entry in result.entries:
        print(f"[{entry.timestamp.isoformat()}] {entry.severity}: {entry.message} (Properties: {entry.properties})")
