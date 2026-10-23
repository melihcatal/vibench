import os
import boto3
import time
from botocore.exceptions import ClientError
from typing import Dict, Any, List

LOG_GROUP_NAME = os.getenv('CLOUDWATCH_LOG_GROUP', 'app-logs')
LOG_STREAM_NAME = os.getenv('CLOUDWATCH_LOG_STREAM', 'default')
REGION = os.getenv('AWS_REGION', 'us-east-1')

logs_client = boto3.client('logs', region_name=REGION)

def ensure_log_stream():
    try:
        logs_client.describe_log_streams(logGroupName=LOG_GROUP_NAME, logStreamNames=[LOG_STREAM_NAME])
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            logs_client.create_log_stream(logGroupName=LOG_GROUP_NAME, logStreamName=LOG_STREAM_NAME)

def append_log_event(message: str) -> Dict[str, Any]:
    ensure_log_stream()
    timestamp = int(time.time() * 1000)
    log_events = [{'timestamp': timestamp, 'message': message}]
    args = {
        'logGroupName': LOG_GROUP_NAME,
        'logStreamName': LOG_STREAM_NAME,
        'logEvents': log_events,
    }
    while True:
        try:
            return logs_client.put_log_events(**args)
        except ClientError as err:
            error_code = err.response['Error']['Code']
            if error_code == 'InvalidSequenceTokenException':
                args['sequenceToken'] = err.response['expectedSequenceToken']
            elif error_code == 'ResourceNotFoundException':
                ensure_log_stream()
            else:
                raise

def run_log_query(start_time: int, end_time: int, query_string: str) -> List[Dict[str, Any]]:
    q_start = logs_client.start_query(
        logGroupName=LOG_GROUP_NAME,
        startTime=start_time,
        endTime=end_time,
        queryString=query_string
    )
    query_id = q_start['queryId']
    while True:
        time.sleep(0.5)
        q_resp = logs_client.get_query_results(queryId=query_id)
        status = q_resp['status']
        if status in ['Complete', 'Failed', 'TimedOut', 'Cancelled']:
            if status == 'Complete':
                return q_resp.get('results', [])
            else:
                raise ValueError(f"Query {status}: {q_resp.get('statistics', {})}")
