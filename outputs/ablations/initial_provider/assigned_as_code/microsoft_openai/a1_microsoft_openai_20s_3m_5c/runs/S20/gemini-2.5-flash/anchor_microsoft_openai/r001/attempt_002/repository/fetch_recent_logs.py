import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from observability_client import AzureMonitorClient
from observability_models import LogEntry, QueryResults

def fetch_recent_logs(time_range_minutes: int = 60, filters: Optional[Dict[str, str]] = None, config: Optional[Dict[str, Any]] = None) -> QueryResults:
    config = config or {}
    client = AzureMonitorClient(
        workspace_id=config.get("AZURE_MONITOR_WORKSPACE_ID"),
        rule_id=config.get("AZURE_MONITOR_RULE_ID"),
        stream_name=config.get("AZURE_MONITOR_STREAM_NAME"),
        logging_endpoint=config.get("AZURE_MONITOR_LOGGING_ENDPOINT"),
        query_endpoint=config.get("AZURE_MONITOR_QUERY_ENDPOINT")
    )

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=time_range_minutes)

    kusto_query = f"""
    {client.stream_name}_CL
    | where TimeGenerated between (datetime('{start_time.isoformat()}')..datetime('{end_time.isoformat()}'))
    """

    if filters:
        for field, value in filters.items():
            kusto_query += f"\n    | where {field}_s == '{value}'"

    kusto_query += f"\n    | project TimeGenerated, message_s, severity_s, correlationId_g, * " # Include all custom columns
    kusto_query += f"\n    | order by TimeGenerated desc"
    
    return client.query_logs(kusto_query, start_time, end_time)
