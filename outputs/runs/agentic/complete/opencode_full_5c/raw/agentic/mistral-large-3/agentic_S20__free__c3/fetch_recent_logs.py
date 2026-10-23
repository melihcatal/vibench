import os
from datetime import datetime, timedelta
from typing import Dict, List
from observability_client import get_logging_client
from observability_models import LogFetchFilter


def fetch_recent_logs(filter: LogFetchFilter) -> List[Dict]:
    """Retrieve recent logs from Azure Monitor Logs filtered by field values and time range."""
    client = get_logging_client()

    # Calculate time range
    end_time = datetime.utcnow()
    start_time = end_time - timedelta(seconds=filter.time_range_seconds)

    # Build the KQL query for Azure Monitor Logs
    field_conditions = " and ".join(
        [f"{k} == '{v}'" for k, v in filter.field_filters.items()]
    )
    query = (
        f"{filter.log_table} "
        f"| where TimeGenerated between (datetime({start_time.isoformat()}) .. datetime({end_time.isoformat()})) "
        f"{f'| where {field_conditions}' if field_conditions else ''} "
        f"| take {filter.limit}"
    )

    # Execute the query
    response = client.query_workspace(
        workspace_id=os.getenv("AZURE_LOG_ANALYTICS_WORKSPACE_ID"),
        query=query,
        timespan=(start_time, end_time),
    )

    logs = []
    for row in response.tables[0].rows:
        logs.append(dict(zip(response.tables[0].columns, row)))

    return logs
