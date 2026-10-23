import boto3
import json
import os
import time

def write_structured_log(log_group_name: str, log_stream_name: str, message: dict):
    client = boto3.client('logs', region_name=os.environ.get('AWS_REGION', 'us-east-1'))

    log_event = {
        'timestamp': int(time.time() * 1000),
        'message': json.dumps(message)
    }

    response = client.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=[log_event]
    )
    return response

if __name__ == '__main__':
    # Example usage (replace with actual log group and stream names)
    LOG_GROUP = os.environ.get('LOG_GROUP_NAME', 'my-application-logs')
    LOG_STREAM = os.environ.get('LOG_STREAM_NAME', 'my-instance-stream')

    # Ensure log group and stream exist (optional, boto3 will create them if not present with put_log_events)
    # client = boto3.client('logs', region_name=os.environ.get('AWS_REGION', 'us-east-1'))
    # try:
    #     client.create_log_group(logGroupName=LOG_GROUP)
    # except client.exceptions.ResourceAlreadyExistsException:
    #     pass
    # try:
    #     client.create_log_stream(logGroupName=LOG_GROUP, logStreamName=LOG_STREAM)
    # except client.exceptions.ResourceAlreadyExistsException:
    #     pass

    structured_log_message = {
        "level": "INFO",
        "service": "user-service",
        "event": "user_login",
        "user_id": "12345",
        "ip_address": "192.168.1.1",
        "timestamp": time.time()
    }
    response = write_structured_log(LOG_GROUP, LOG_STREAM, structured_log_message)
    print(f"Log event written: {response}")
