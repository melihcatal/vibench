import boto3
import json
import os
import time

def write_structured_log(log_group_name: str, log_stream_name: str, message: dict):
    client = boto3.client("logs", region_name=os.environ.get("AWS_REGION", "us-east-1"))
    
    log_event = {
        "timestamp": int(time.time() * 1000),
        "message": json.dumps(message)
    }

    try:
        # Ensure log group and stream exist
        try:
            client.create_log_group(logGroupName=log_group_name)
        except client.exceptions.ResourceAlreadyExistsException:
            pass
        try:
            client.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
        except client.exceptions.ResourceAlreadyExistsException:
            pass

        response = client.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=[log_event]
        )
        return response
    except Exception as e:
        print(f"Error writing structured log: {e}")
        raise
