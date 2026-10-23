from datetime import datetime
import time
from typing import Dict, Any, List, Optional
import boto3
from observability_models import FilteredLogEntry

def fetch_recent_logs(log_group_name: str, start_time_ms: int, end_time_ms: int, filter_pattern: Optional[str] = None, config: Dict[str, Any] = None) -> List[FilteredLogEntry]:
    config = config or {}
    client = boto3.client("logs", region_name=config.get("region"))

    query_string = "fields @timestamp, @message | sort @timestamp desc"
    if filter_pattern:
        query_string += f" | filter @message like /{filter_pattern}/"

    start_query_response = client.start_query(
        logGroupName=log_group_name,
        startTime=int(start_time_ms / 1000),  # CloudWatch expects seconds
        endTime=int(end_time_ms / 1000),      # CloudWatch expects seconds
        queryString=query_string,
        limit=100  # Default limit
    )

    query_id = start_query_response['queryId']

    response = None
    while response is None or response['status'] == 'Running':
        time.sleep(1)
        response = client.get_query_results(queryId=query_id)

    recent_logs = []
    for result in response['results']:
        timestamp = None
        message = None
        for field in result:
            if field['field'] == '@timestamp':
                timestamp_str = field['value']
                dt_object = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
                timestamp = int(dt_object.timestamp() * 1000)
            elif field['field'] == '@message':
                message = field['value']
        if timestamp and message:
            recent_logs.append(FilteredLogEntry(
                timestamp=timestamp,
                message=message,
                log_stream_name="N/A",
                log_group_name=log_group_name
            ))
    return recent_logs
