import boto3
import os
from observability_client import CLOUDWATCH_LOG_GROUP, CLOUDWATCH_LOG_STREAM, put_log_events
from observability_models import StructuredLog, to_cloudwatch_event

def write_structured_log(level: str, message: str, service: str):
    log = StructuredLog(level=level, message=message, service=service)
    event = to_cloudwatch_event(log)
    client = boto3.client('logs', region_name=os.getenv('AWS_REGION', 'us-east-1'))
    next_token = put_log_events(client, CLOUDWATCH_LOG_GROUP, CLOUDWATCH_LOG_STREAM, [event])
    return next_token
