import os
from datetime import timedelta
from azure.monitor.query import LogsQueryStatus
from observability_client import get_query_client
from observability_models import LogQueryResponse

def fetch_recent_logs(field_filters: dict[str, str], timespan_minutes: int = 60):
    client = get_query_client()
    workspace_id = os.environ.get("AZURE_LOG_ANALYTICS_WORKSPACE_ID")

    if not workspace_id:
        raise ValueError("Missing Azure Log Analytics Workspace ID environment variable: AZURE_LOG_ANALYTICS_WORKSPACE_ID")

    filter_clauses = []
    for field, value in field_filters.items():
        filter_clauses.append(f'{field} == "{value}"')
    
    where_clause = " and ".join(filter_clauses)

    query = f"""
    <YOUR_LOG_TABLE_NAME>
    | where {where_clause}
    | order by TimeGenerated desc
    """
    # Replace <YOUR_LOG_TABLE_NAME> with the actual table name you are ingesting to, e.g., 'MyCustomLog_CL'

    response = client.query_workspace(
        workspace_id=workspace_id,
        query=query,
        timespan=timedelta(minutes=timespan_minutes)
    )

    if response.status == LogsQueryStatus.SUCCESS:
        return LogQueryResponse(tables=[table.as_dict() for table in response.tables])
    else:
        raise Exception(f"Query failed with status: {response.status}, error: {response.error}")
