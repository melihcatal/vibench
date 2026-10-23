from datetime import datetime, timedelta
from typing import Dict, Any
from observability_client import ObservabilityClient
from observability_models import QueryParameters, LogQueryResponse
from azure.monitor.query import LogsQueryStatus

def query_error_logs(config: Dict[str, Any], time_range_minutes: int = 60) -> LogQueryResponse:
    client_wrapper = ObservabilityClient(ingestion_endpoint="", query_endpoint="https://api.loganalytics.io") # Ingestion endpoint not needed for query
    query_client = client_wrapper.get_query_client()

    workspace_id = config['workspace_id']
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=time_range_minutes)

    # Kusto Query Language (KQL)
    query = f"""
    {config.get('log_table', 'AppEvents')}
    | where Severity == 'Error'
    | where TimeGenerated between (datetime('{start_time.isoformat()}Z') .. datetime('{end_time.isoformat()}Z'))
    | order by TimeGenerated desc
    """

    response = query_client.query_workspace(
        workspace_id=workspace_id,
        query=query,
        timespan=timedelta(minutes=time_range_minutes)
    )

    if response.status == LogsQueryStatus.PARTIAL_FAILURE:
        print(f"Query returned partial data: {response.partial_error}")

    return LogQueryResponse(tables=response.tables)
