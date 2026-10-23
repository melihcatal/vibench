import boto3
import json
import os
import time
from typing import List, Dict

def write_correlated_logs(log_group_name: str, log_stream_name: str, correlation_id: str, messages: List[Dict]):
    client = boto3.client("logs", region_name=os.environ.get("AWS_REGION", "us-east-1"))
    
    log_events = []
    for msg in messages:
        msg["correlation_id"] = correlation_id
        log_events.append({
            "timestamp": int(time.time() * 1000),
            "message": json.dumps(msg)
        })

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
            logEvents=log_events
        )
        return response
    except Exception as e:
        print(f"Error writing correlated logs: {e}")
        raise
