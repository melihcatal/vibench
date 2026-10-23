import os
import time
from observability_client import clients
from typing import List, Dict, Any

def write_correlated_logs(
    log_group_name: str,
    correlation_id: str,
    log_events: List[Dict[str, Any]],
    log_stream_name: str = "default-stream"
):
    """
    Writes application log events with a shared correlation identifier to AWS CloudWatch Logs.
    Each event's message will include the correlation_id.
    """
    aws_logs_client = clients.aws_logs_client

    try:
        aws_logs_client.create_log_group(logGroupName=log_group_name)
    except aws_logs_client.exceptions.ResourceAlreadyExistsException:
        pass
    
    sequence_token = None
    try:
        response = aws_logs_client.describe_log_streams(
            logGroupName=log_group_name,
            logStreamNamePrefix=log_stream_name
        )
        for stream in response.get("logStreams", []):
            if stream["logStreamName"] == log_stream_name:
                sequence_token = stream.get("uploadSequenceToken")
                break
        if sequence_token is None:
            aws_logs_client.create_log_stream(
                logGroupName=log_group_name,
                logStreamName=log_stream_name
            )
    except aws_logs_client.exceptions.ResourceNotFoundException:
        aws_logs_client.create_log_stream(
            logGroupName=log_group_name,
            logStreamName=log_stream_name
        )
    
    processed_events = []
    for event in log_events:
        event_message = event.get("message", "")
        processed_event = {
            "timestamp": int(time.time() * 1000),
            "message": f"[{correlation_id}] {event_message}"
        }
        processed_events.append(processed_event)

    processed_events.sort(key=lambda x: x["timestamp"])

    put_log_events_kwargs = {
        "logGroupName": log_group_name,
        "logStreamName": log_stream_name,
        "logEvents": processed_events
    }
    if sequence_token:
        put_log_events_kwargs["sequenceToken"] = sequence_token

    response = aws_logs_client.put_log_events(**put_log_events_kwargs)
    return response
