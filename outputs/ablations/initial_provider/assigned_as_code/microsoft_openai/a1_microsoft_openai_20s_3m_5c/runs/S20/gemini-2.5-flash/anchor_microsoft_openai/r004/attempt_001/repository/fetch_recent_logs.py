import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from observability_client import ObservabilityClient
from observability_models import LogQueryResult

def fetch_recent_logs(
    time_range_minutes: int = 60,
    filter_field: Optional[str] = None,
    filter_value: Optional[str] = None,
    config: Dict[str, Any] = None
) -> List[LogQueryResult]:
    config = config or {}
    observability_client = ObservabilityClient(config)
    query_client = observability_client.get_logs_query_client()
    workspace_id = observability_client.log_analytics_workspace_id

    if not workspace_id:
        raise ValueError("Log Analytics Workspace ID not configured.")

    query_parts = [
        "MyApplicationLogs_CL",
        f"| where TimeGenerated > ago({time_range_minutes}m)"
    ]

    if filter_field and filter_value:
        # Assuming that fields in custom logs might have a _s suffix for string types
        # Adjust column names based on your actual log schema in Azure Monitor
        query_parts.append(f"| where {filter_field}_s has '{filter_value}'")

    query_parts.append("| project TimeGenerated, message, severity_s, properties_s")
    query_parts.append("| order by TimeGenerated desc")

    query = "\n".join(query_parts)

    response = query_client.query_workspace(
        workspace_id=workspace_id,
        query=query,
        timespan=timedelta(minutes=time_range_minutes)
    )

    results: List[LogQueryResult] = []
    for table in response.tables:
        for row in table.rows:
            timestamp_str = row[0]
            message = row[1]
            severity = row[2]
            properties_str = row[3]

            timestamp = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00')) if isinstance(timestamp_str, str) else timestamp_str

            results.append(LogQueryResult(
                timestamp=timestamp,
                message=message,
                severity=severity,
                # properties=json.loads(properties_str) if properties_str else {}
            ))
    return results
