from typing import Any, Dict, List

import boto3
from botocore.exceptions import ClientError


def create_log_group(log_group_name: str) -> None:
    cloudwatch_logs = boto3.client('logs')
    try:
        cloudwatch_logs.create_log_group(logGroupName=log_group_name)
        print(f'Log group {log_group_name} created successfully.')
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceAlreadyExistsException':
            print(f'Log group {log_group_name} already exists.')
        else:
            print(f'Failed to create log group {log_group_name}: {e}')


def put_log_events(log_group_name: str, log_stream_name: str, log_events: List[Dict[str, Any]]) -> None:
    cloudwatch_logs = boto3.client('logs')
    try:
        cloudwatch_logs.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=log_events
        )
        print(f'Log events added to {log_group_name}/{log_stream_name} successfully.')
    except ClientError as e:
        print(f'Failed to put log events: {e}')


def normalize_log_event(log_event: Dict[str, Any]) -> Dict[str, Any]:
    normalized_event = {
        'timestamp': log_event.get('timestamp', 0),
        'message': log_event.get('message', '')
    }
    return normalized_event


def main() -> None:
    log_group_name = 'my-log-group'
    log_stream_name = 'my-log-stream'
    log_events = [
        {
            'timestamp': int(time.time() * 1000),
            'message': 'This is a log message.'
        },
        {
            'timestamp': int(time.time() * 1000) + 1000,
            'message': 'This is another log message.'
        }
    ]

    create_log_group(log_group_name)
    normalized_log_events = [normalize_log_event(event) for event in log_events]
    put_log_events(log_group_name, log_stream_name, normalized_log_events)


if __name__ == '__main__':
    main()