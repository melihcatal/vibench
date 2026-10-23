import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from observability_client import AzureMonitorClient
from observability_models import LogEntry, QueryResults

def query_error_logs(severity: str = "Error", time_range_minutes: int = 60, config: Optional[Dict[str, Any]] = None) -> QueryResults:
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

    # Assuming CustomLog is the table name where logs are ingested
    # And 'severity' and 'message' are columns in the CustomLog table.
    kusto_query = f"""
    {client.stream_name}_CL
    | where severity_s == '{severity}'
    | where TimeGenerated between (datetime('{start_time.isoformat()}')..datetime('{end_time.isoformat()}'))
    | project TimeGenerated, message_s, severity_s, correlationId_g
    | order by TimeGenerated desc
    """
    
    return client.query_logs(kusto_query, start_time, end_time)
