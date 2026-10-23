from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from observability_client import ObservabilityClient
from observability_models import LogQueryResponse
from azure.monitor.query import LogsQueryStatus

def fetch_recent_logs(config: Dict[str, Any], time_range_minutes: int = 60, filters: Optional[Dict[str, str]] = None) -> LogQueryResponse:
    client_wrapper = ObservabilityClient(ingestion_endpoint="", query_endpoint="https://api.loganalytics.io")
    query_client = client_wrapper.get_query_client()

    workspace_id = config['workspace_id']
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(minutes=time_range_minutes)

    log_table = config.get('log_table', 'AppEvents')
    query_parts = [
        f"{log_table}",
        f"where TimeGenerated between (datetime('{start_time.isoformat()}Z') .. datetime('{end_time.isoformat()}Z'))"
    ]

    if filters:
        for field, value in filters.items():
            query_parts.append(f"where {field} contains '{{value}}'")

    query_parts.append("order by TimeGenerated desc")
    query = " | ".join(query_parts)

    response = query_client.query_workspace(
        workspace_id=workspace_id,
        query=query,
        timespan=timedelta(minutes=time_range_minutes)
    )

    if response.status == LogsQueryStatus.PARTIAL_FAILURE:
        print(f"Query returned partial data: {response.partial_error}")

    return LogQueryResponse(tables=response.tables)
