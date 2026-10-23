from datetime import datetime, timedelta
from typing import List, Dict, Any
from observability_client import ObservabilityClient
from observability_models import LogEntry, LogQueryResult
from azure.monitor.query import LogsQueryStatus
import json

def fetch_recent_logs(
    time_range_minutes: int = 60,
    filter_field: Optional[str] = None,
    filter_value: Optional[Any] = None,
    severity_filter: Optional[str] = None
) -> LogQueryResult:
    client = ObservabilityClient()
    logs_query_client = client.get_logs_query_client()
    workspace_id = client.get_log_analytics_workspace_id()

    if not logs_query_client or not workspace_id:
        print("Azure Log Analytics client not configured. Cannot fetch recent logs.")
        return LogQueryResult([], datetime.utcnow(), 0)

    query_parts = [
        f"traces",
        f"where TimeGenerated > ago({time_range_minutes}m)"
    ]

    if severity_filter:
        # SeverityLevel mapping: 0: Verbose, 1: Information, 2: Warning, 3: Error, 4: Critical
        severity_map = {
            "VERBOSE": '0',
            "INFO": '1',
            "WARNING": '2',
            "ERROR": '3',
            "CRITICAL": '4'
        }
        kql_severity = severity_map.get(severity_filter.upper())
        if kql_severity is not None:
            query_parts.append(f"where SeverityLevel == '{kql_severity}'")
        else:
            print(f"Warning: Unknown severity_filter '{severity_filter}'. Ignoring filter.")

    if filter_field and filter_value is not None:
        # For custom dimensions, we need to parse CustomDimensions JSON string
        # This example assumes the filter_field is directly available or within CustomDimensions
        # A more robust solution might involve parsing CustomDimensions dynamically if not a direct column
        if filter_field.lower() == "correlation_id": # Assuming correlation_id is a direct property or custom dimension
             query_parts.append(f"where tostring(CustomDimensions.correlation_id) == '{filter_value}'")
        else:
             query_parts.append(f"where tostring(CustomDimensions.{filter_field}) == '{filter_value}' or {filter_field} == '{filter_value}'")

    query_parts.append("project TimeGenerated, Message=AppMessage, Severity=SeverityLevel, CustomDimensions")
    query_parts.append("order by TimeGenerated desc")

    query = "\n| ".join(query_parts)
    
    print(f"Executing KQL query:\n{query}")

    try:
        response = logs_query_client.query_workspace(workspace_id, query, timespan=None)

        if response.status == LogsQueryStatus.SUCCESS:
            recent_entries: List[LogEntry] = []
            total_count = 0
            for table in response.tables:
                total_count += len(table.rows)
                for row in table.rows:
                    time_generated = row[table.columns.index("TimeGenerated")]
                    message = row[table.columns.index("Message")]
                    severity_level = row[table.columns.index("Severity")]
                    custom_dimensions_str = row[table.columns.index("CustomDimensions")]

                    severity_map = {'0': 'VERBOSE', '1': 'INFO', '2': 'WARNING', '3': 'ERROR', '4': 'CRITICAL'}
                    severity = severity_map.get(str(severity_level), 'UNKNOWN')

                    properties = {}
                    if custom_dimensions_str:
                        try:
                            properties = json.loads(custom_dimensions_str)
                        except json.JSONDecodeError:
                            pass
                    
                    correlation_id = properties.get("correlation_id") # Extract correlation_id if present in custom dimensions

                    recent_entries.append(LogEntry(
                        message=message,
                        severity=severity,
                        timestamp=time_generated,
                        properties=properties,
                        correlation_id=correlation_id
                    ))
            print(f"Found {len(recent_entries)} recent logs matching criteria.")
            return LogQueryResult(recent_entries, datetime.utcnow(), total_count)
        else:
            print(f"Log query failed with status: {response.status}. Error: {response.partial_error}")
            return LogQueryResult([], datetime.utcnow(), 0)
    except Exception as e:
        print(f"An error occurred during log query: {e}")
        return LogQueryResult([], datetime.utcnow(), 0)

if __name__ == "__main__":
    # Example usage:
    print("Fetching all recent logs (last 60 minutes):")
    all_logs = fetch_recent_logs()
    for entry in all_logs.entries:
        print(f"[{entry.timestamp.isoformat()}] {entry.severity}: {entry.message} (Correlation ID: {entry.correlation_id}, Props: {entry.properties})")

    print("\nFetching recent ERROR logs (last 30 minutes):")
    error_logs = fetch_recent_logs(time_range_minutes=30, severity_filter="ERROR")
    for entry in error_logs.entries:
        print(f"[{entry.timestamp.isoformat()}] {entry.severity}: {entry.message} (Correlation ID: {entry.correlation_id}, Props: {entry.properties})")

    print("\nFetching logs with specific correlation ID (last 120 minutes):")
    # Replace with a real correlation_id from your logs if testing
    sample_correlation_id = "your-sample-correlation-id"
    correlated_logs = fetch_recent_logs(time_range_minutes=120, filter_field="correlation_id", filter_value=sample_correlation_id)
    if correlated_logs.entries:
        for entry in correlated_logs.entries:
            print(f"[{entry.timestamp.isoformat()}] {entry.severity}: {entry.message} (Correlation ID: {entry.correlation_id}, Props: {entry.properties})")
    else:
        print(f"No logs found for correlation ID: {sample_correlation_id}")
