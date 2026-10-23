from datetime import datetime, timezone, timedelta
from typing import Dict, Any
from observability_client import ObservabilityClient

def fetch_recent_logs(filters: Dict[str, Any], duration_hours: int = 24) -> list[dict]:
    client = ObservabilityClient()

    # Start with a base query on our assumed custom log table
    query_parts = ["MyPythonLogs_CL"]

    for field, value in filters.items():
        # For string values, use 'contains' or '==' for exact match. Here, we'll use '==' for exact match
        # For simplicity, assuming all filter values are directly comparable as strings or numbers.
        if isinstance(value, str):
            query_parts.append(f"where {field} == '{value}'")
        else:
            query_parts.append(f"where {field} == {value}")
    
    # Add ordering for recent logs
    query_parts.append("order by TimeGenerated desc")

    kusto_query = " | ".join(query_parts)
    
    recent_logs = client.query_logs(query=kusto_query, duration_hours=duration_hours)
    return recent_logs
