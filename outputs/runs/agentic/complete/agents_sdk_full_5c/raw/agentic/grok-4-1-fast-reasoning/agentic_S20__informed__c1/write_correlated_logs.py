import boto3
from typing import List, Dict, Any
from observability_client import get_cloudwatch_config, create_correlated_log_events
from observability_models import StructuredLogData, LogEvent

def write_correlated_logs(events: List[StructuredLogData], correlation_id: str):
    config = get_cloudwatch_config()
    client = boto3.client('logs', region_name=config['region'])
    log_events: List[LogEvent] = create_correlated_log_events(events, correlation_id)
    response = client.put_log_events(
        logGroupName=config['log_group'],
        logStreamName=config['log_stream'],
        logEvents=log_events
    )
    print(f"Wrote correlated logs: {response['nextSequenceToken']}")
