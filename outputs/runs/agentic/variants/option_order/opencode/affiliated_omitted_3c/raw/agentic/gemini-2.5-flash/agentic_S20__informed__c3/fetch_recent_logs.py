import time
from datetime import datetime, timedelta
from typing import List, Dict, Any
from observability_client import CloudWatchLogsClient
from observability_models import LogQuery, LogQueryResult

def fetch_recent_logs(
    log_group_names: List[str],
    start_time: datetime,
    end_time: datetime,
    filter_field: str = None,
    filter_value: str = None,
    limit: int = 50
) -> LogQueryResult:
    """Retrieves recent log results from AWS CloudWatch Logs filtered by field values and time range.

    Args:
        log_group_names: A list of CloudWatch log group names to query.
        start_time: The start time for the query.
        end_time: The end time for the query.
        filter_field: An optional field name to filter by.
        filter_value: An optional value to match in the filter_field.
        limit: The maximum number of log events to retrieve.

    Returns:
        A LogQueryResult object containing the query results and status.
    """
    client = CloudWatchLogsClient()

    query_string = f"fields @timestamp, @message | sort @timestamp desc | limit {limit}"

    if filter_field and filter_value:
        # Assuming the structured log message is a string representation of a JSON object
        query_string = (
            f"fields @timestamp, @message | filter @message like /\"{filter_field}\":\""
            f"{filter_value}\"/
            | sort @timestamp desc
            | limit {limit}"
        )

    start_time_ms = int(start_time.timestamp() * 1000)
    end_time_ms = int(end_time.timestamp() * 1000)

    start_query_response = client.start_query(
        log_group_names=log_group_names,
        startTime=start_time_ms,
        endTime=end_time_ms,
        queryString=query_string
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

    normalized_records = []
    for record in records:
        normalized_record = {}
        for field in record:
            normalized_record[field['field']] = field['value']
        normalized_records.append(normalized_record)

    return LogQueryResult(records=normalized_records, status=status, query_id=query_id)
