import boto3
import os
from observability_client import CLOUDWATCH_LOG_GROUP, CLOUDWATCH_LOG_STREAM, put_log_events
from observability_models import StructuredLog, to_cloudwatch_event

def write_correlated_logs(correlation_id: str):
    logs = [
        StructuredLog(level='INFO', message=f'Request {correlation_id} started', service='web', correlation_id=correlation_id),
        StructuredLog(level='INFO', message=f'Processing request {correlation_id}', service='web', correlation_id=correlation_id),
        StructuredLog(level='ERROR', message=f'Failed to process {correlation_id}', service='web', correlation_id=correlation_id),
    ]
    events = [to_cloudwatch_event(log) for log in logs]
    client = boto3.client('logs', region_name=os.getenv('AWS_REGION', 'us-east-1'))
    next_token = put_log_events(client, CLOUDWATCH_LOG_GROUP, CLOUDWATCH_LOG_STREAM, events)
    return next_token
