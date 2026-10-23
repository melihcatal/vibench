from datetime import datetime
import time
from typing import Dict, Any, List
import boto3
from observability_models import FilteredLogEntry, LogGroupConfig

def query_error_logs(log_group_name: str, start_time_ms: int, end_time_ms: int, config: Dict[str, Any] = None) -> List[FilteredLogEntry]:
    config = config or {}
    client = boto3.client("logs", region_name=config.get("region"))

    query_string = "fields @timestamp, @message | filter @message like /\"severity\":\"ERROR\"/ | sort @timestamp desc"

    start_query_response = client.start_query(
        logGroupName=log_group_name,
        startTime=int(start_time_ms / 1000), # CloudWatch expects seconds
        endTime=int(end_time_ms / 1000),     # CloudWatch expects seconds
        queryString=query_string,
        limit=100  # Default limit
    )

    query_id = start_query_response['queryId']

    response = None
    while response is None or response['status'] == 'Running':
        time.sleep(1)
        response = client.get_query_results(queryId=query_id)

    error_logs = []
    for result in response['results']:
        timestamp = None
        message = None
        for field in result:
            if field['field'] == '@timestamp':
                # CloudWatch returns ISO format, convert to milliseconds
                timestamp_str = field['value']
                dt_object = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
                timestamp = int(dt_object.timestamp() * 1000)
            elif field['field'] == '@message':
                message = field['value']
        if timestamp and message:
            error_logs.append(FilteredLogEntry(
                timestamp=timestamp,
                message=message,
                log_stream_name="N/A",  # Not directly available from query results fields
                log_group_name=log_group_name
            ))
    return error_logs
