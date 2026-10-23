import os
from datetime import datetime, timedelta
from observability_client import get_logs_query_client
from observability_models import QueryResult


def query_error_logs(workspace_id: str, severity: str, time_range_minutes: int) -> QueryResult:
    client = get_logs_query_client()

    # Kusto Query Language (KQL)
    query = (
        f"let timeRange = ago({time_range_minutes}m); "
        f"AzureActivity "
        f"| where Level == \'{severity}\' "
        f"| where TimeGenerated > timeRange "
        f"| project TimeGenerated, OperationName, Level, ActivityStatus, ResourceGroup, _ResourceId, Caller"
    )

    response = client.query_workspace(workspace_id=workspace_id, query=query, timespan=timedelta(minutes=time_range_minutes))

    tables_data = []
    for table in response.tables:
        columns = [col.name for col in table.columns]
        rows = []
        for row_data in table.rows:
            rows.append(dict(zip(columns, row_data)))
        tables_data.append({"name": table.name, "columns": columns, "rows": rows})

    return QueryResult(tables=tables_data)
