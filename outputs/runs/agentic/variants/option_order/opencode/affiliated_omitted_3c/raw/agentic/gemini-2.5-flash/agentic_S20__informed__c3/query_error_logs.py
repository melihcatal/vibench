import time
from datetime import datetime, timedelta
from typing import List, Dict, Any
from observability_client import CloudWatchLogsClient
from observability_models import LogQuery, LogQueryResult

def query_error_logs(
    log_group_names: List[str],
    start_time: datetime,
    end_time: datetime,
    severity_level: str = "ERROR",
    limit: int = 20
) -> LogQueryResult:
    """Queries recent error log entries from AWS CloudWatch Logs filtered by severity and time range.

    Args:
        log_group_names: A list of CloudWatch log group names to query.
        start_time: The start time for the query.
        end_time: The end time for the query.
        severity_level: The severity level to filter by (default: ERROR).
        limit: The maximum number of log events to retrieve.

    Returns:
        A LogQueryResult object containing the query results and status.
    """
    client = CloudWatchLogsClient()

    query_string = (
        f"fields @timestamp, @message | filter @message like /\"level\":\"" \
        f"{severity_level}\"/
        | sort @timestamp desc
        | limit {limit}"
    )

    # Convert datetime to milliseconds Unix timestamp
    start_time_ms = int(start_time.timestamp() * 1000)
    end_time_ms = int(end_time.timestamp() * 1000)

    start_query_response = client.start_query(
        log_group_names=log_group_names,
        start_time=start_time_ms,
        end_time=end_time_ms,
        query_string=query_string
    )

    query_id = start_query_response['queryId']

    status = 'Running'
    records = []

    while status in ['Running', 'Scheduled']:
        time.sleep(1)  # Wait for 1 second before checking results again
        query_results_response = client.get_query_results(query_id=query_id)
        status = query_results_response['status']
        if 'results' in query_results_response:
            records = query_results_response['results']

    # Normalize the results into a more consumable format
    normalized_records = []
    for record in records:
        normalized_record = {}
        for field in record:
            normalized_record[field['field']] = field['value']
        normalized_records.append(normalized_record)

    return LogQueryResult(records=normalized_records, status=status, query_id=query_id)
