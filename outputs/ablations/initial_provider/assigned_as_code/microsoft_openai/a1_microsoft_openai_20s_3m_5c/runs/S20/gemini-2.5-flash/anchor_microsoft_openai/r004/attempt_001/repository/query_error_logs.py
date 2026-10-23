import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
from observability_client import ObservabilityClient
from observability_models import LogQueryResult

def query_error_logs(time_range_minutes: int = 60, config: Dict[str, Any] = None) -> List[LogQueryResult]:
    config = config or {}
    observability_client = ObservabilityClient(config)
    query_client = observability_client.get_logs_query_client()
    workspace_id = observability_client.log_analytics_workspace_id

    if not workspace_id:
        raise ValueError("Log Analytics Workspace ID not configured.")

    # Kusto Query Language (KQL) to query error logs
    # Assuming custom log table for ingested logs is named 'MyCorrelatedLogs_CL' or similar.
    # For simplicity, let's assume logs are ingested into a custom table named `MyApplicationLogs_CL`
    # and it has columns like `TimeGenerated`, `message`, `severity`.
    # You might need to adjust the table name and column names based on your actual Azure Monitor setup.
    query = f"""
    MyApplicationLogs_CL
    | where TimeGenerated > ago({time_range_minutes}m)
    | where severity_s == 'Error' or severity_s == 'Critical'
    | project TimeGenerated, message, severity_s, properties_s
    | order by TimeGenerated desc
    """

    response = query_client.query_workspace(
        workspace_id=workspace_id,
        query=query,
        timespan=timedelta(minutes=time_range_minutes)
    )

    results: List[LogQueryResult] = []
    for table in response.tables:
        for row in table.rows:
            # Assuming the order of columns matches the project statement in KQL
            timestamp_str = row[0] # TimeGenerated
            message = row[1]       # message
            severity = row[2]      # severity_s
            properties_str = row[3] # properties_s as a string

            # Azure Log Analytics returns datetime objects, but they might be strings depending on client library version
            # Ensure conversion to datetime object if it's a string
            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00')) if isinstance(timestamp_str, str) else timestamp_str

            results.append(LogQueryResult(
                timestamp=timestamp,
                message=message,
                severity=severity,
                # properties=json.loads(properties_str) if properties_str else {}
            ))
    return results
