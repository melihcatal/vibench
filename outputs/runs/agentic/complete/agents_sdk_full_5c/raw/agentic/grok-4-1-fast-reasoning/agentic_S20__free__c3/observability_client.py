import os
import time
from typing import List, Dict, Any

CLOUDWATCH_REGION = os.getenv('AWS_REGION', 'us-east-1')
CLOUDWATCH_LOG_GROUP = os.getenv('CLOUDWATCH_LOG_GROUP', '/myapp/logs')
CLOUDWATCH_LOG_STREAM = os.getenv('CLOUDWATCH_LOG_STREAM', 'default')

def get_upload_sequence_token(client, log_group: str, log_stream: str) -> str | None:
    try:
        resp = client.describe_log_streams(
            logGroupName=log_group,
            logStreamNamePrefix=log_stream
        )
        if resp['logStreams']:
            return resp['logStreams'][0].get('uploadSequenceToken')
    except Exception:
        pass
    return None

def put_log_events(client, log_group: str, log_stream: str, events: List[Dict[str, Any]]) -> str:
    seq_token = get_upload_sequence_token(client, log_group, log_stream)
    kwargs = {
        'logGroupName': log_group,
        'logStreamName': log_stream,
        'logEvents': events
    }
    if seq_token:
        kwargs['sequenceToken'] = seq_token
    resp = client.put_log_events(**kwargs)
    return resp['nextSequenceToken']

def execute_query(client, log_group: str, start_time_sec: int, end_time_sec: int, query_string: str) -> List[List[Dict[str, str]]]:
    start_query_resp = client.start_query(
        logGroupName=log_group,
        startTime=start_time_sec,
        endTime=end_time_sec,
        queryString=query_string
    )
    query_id = start_query_resp['queryId']
    
    while True:
        time.sleep(1)
        results_resp = client.get_query_results(queryId=query_id)
        status = results_resp['status']
        if status in ['Complete', 'Failed', 'Cancelled']:
            if status != 'Complete':
                raise ValueError(f"Query {status}: {results_resp.get('errorMessage', 'Unknown error')}")
            return results_resp['results']
