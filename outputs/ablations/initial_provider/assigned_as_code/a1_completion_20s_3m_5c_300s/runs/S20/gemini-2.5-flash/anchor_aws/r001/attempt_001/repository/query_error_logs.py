import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

from observability_client import CloudWatchLogsClient
from observability_models import QueryLogsRequest, QueryLogsResponse

def query_error_logs(
    log_group_name: Optional[str] = None,
    severity: str = "ERROR",
    time_range_minutes: int = 60,
    region_name: Optional[str] = None,
    limit: int = 100
) -> QueryLogsResponse:
    log_group_name = log_group_name or os.environ.get("LOG_GROUP_NAME", "my-application-logs")
    client = CloudWatchLogsClient(region_name=region_name)

    end_time = datetime.now()
    start_time = end_time - timedelta(minutes=time_range_minutes)

    start_time_ms = int(start_time.timestamp() * 1000)
    end_time_ms = int(end_time.timestamp() * 1000)

    # CloudWatch Logs Insights query to filter by severity
    # Assuming the log message is JSON and contains a 'severity' field.
    # For structured logs, the filter pattern can directly refer to fields.
    filter_pattern = f"@message like /\"severity\":\""""""""""{severity}\""""""""""/ or @message like /\"level\":\""""""""""{severity}\""""""""""/"

    query_request = QueryLogsRequest(
        log_group_name=log_group_name,
        start_time_ms=start_time_ms,
        end_time_ms=end_time_ms,
        filter_pattern=filter_pattern,
        limit=limit,
    )

    results = client.query_log_events(query_request)
    return QueryLogsResponse(events=results["events"])
