import os
from datetime import datetime, timedelta
from typing import Dict, Any
from observability_client import get_logs_query_client
from observability_models import QueryResult


def fetch_recent_logs(workspace_id: str, time_range_minutes: int, filters: Dict[str, Any] = None) -> QueryResult:
    client = get_logs_query_client()
    filters = filters or {}

    # Kusto Query Language (KQL)
    query_parts = [
        f"let timeRange = ago({time_range_minutes}m); "
        f"AzureActivity "
        f"| where TimeGenerated > timeRange "
    ]

    for field, value in filters.items():
        # Basic sanitization for field names to prevent KQL injection. 
        # In a production system, a more robust KQL escaping mechanism would be necessary.
        sanitized_field = ''.join(filter(str.isalnum, field)) 
        query_parts.append(f"| where {sanitized_field} == \'{value}\' ")

    query_parts.append(f"| project TimeGenerated, OperationName, Level, ActivityStatus, ResourceGroup, _ResourceId, Caller, Category") # Added Category field as an example

    query = "".join(query_parts)

    response = client.query_workspace(workspace_id=workspace_id, query=query, timespan=timedelta(minutes=time_range_minutes))

    tables_data = []
    for table in response.tables:
        columns = [col.name for col in table.columns]
        rows = []
        for row_data in table.rows:
            rows.append(dict(zip(columns, row_data)))
        tables_data.append({"name": table.name, "columns": columns, "rows": rows})

    return QueryResult(tables=tables_data)
