import boto3
import json
import os
from datetime import datetime
from observability_client import get_cloudwatch_client


def write_structured_log(log_group_name, log_stream_name, log_data):
    """
    Write a structured JSON log event to AWS CloudWatch Logs.

    Args:
        log_group_name: CloudWatch Logs group name
        log_stream_name: CloudWatch Logs stream name
        log_data: Dictionary containing structured log data
    """
    client = get_cloudwatch_client()

    # Add timestamp if not present
    if "timestamp" not in log_data:
        log_data["timestamp"] = int(datetime.now().timestamp() * 1000)

    # Ensure message field exists for CloudWatch
    if "message" not in log_data:
        log_data["message"] = json.dumps(log_data)

    log_event = {"timestamp": log_data["timestamp"], "message": json.dumps(log_data)}

    try:
        # Create log stream if it doesn't exist
        try:
            client.create_log_stream(
                logGroupName=log_group_name, logStreamName=log_stream_name
            )
        except client.exceptions.ResourceAlreadyExistsException:
            pass

        # Put log event
        response = client.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=[log_event],
        )

        return {
            "success": True,
            "nextSequenceToken": response.get("nextSequenceToken"),
            "log_event": log_event,
        }
    except Exception as e:
        return {"success": False, "error": str(e)}
