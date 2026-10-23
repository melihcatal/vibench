import boto3
import os
from typing import Dict, Any
from observability_client import get_cloudwatch_config, create_log_event
from observability_models import StructuredLogData

def write_structured_log(data: StructuredLogData):
    config = get_cloudwatch_config()
    client = boto3.client('logs', region_name=config['region'])
    log_event = create_log_event(data)
    response = client.put_log_events(
        logGroupName=config['log_group'],
        logStreamName=config['log_stream'],
        logEvents=[log_event]
    )
    print(f"Wrote log: {response['nextSequenceToken']}")
