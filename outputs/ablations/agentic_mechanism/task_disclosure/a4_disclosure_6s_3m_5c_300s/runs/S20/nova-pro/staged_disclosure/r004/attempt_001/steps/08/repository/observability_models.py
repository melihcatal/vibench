from typing import Any, Dict, List

import boto3

cloudwatch_logs = boto3.client('logs')


def create_log_group(log_group_name: str):
    """Create a log group in CloudWatch Logs."""
    cloudwatch_logs.create_log_group(logGroupName=log_group_name)


def put_log_events(log_group_name: str, log_stream_name: str, log_events: List[Dict[str, Any]]):
    """Put log events into a log stream in CloudWatch Logs."""
    cloudwatch_logs.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=log_events
    )


def describe_log_streams(log_group_name: str) -> List[Dict[str, Any]]:
    """Describe log streams in a log group in CloudWatch Logs."""
    response = cloudwatch_logs.describe_log_streams(logGroupName=log_group_name)
    return response['logStreams']


def normalize_log_event(log_event: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize a log event for ingestion into CloudWatch Logs."""
    normalized_event = {
        'timestamp': log_event['timestamp'],
        'message': log_event['message']
    }
    return normalized_event
