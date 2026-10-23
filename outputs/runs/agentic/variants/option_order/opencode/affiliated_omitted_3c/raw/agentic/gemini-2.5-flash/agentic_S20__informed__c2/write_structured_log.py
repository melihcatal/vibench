import json
import os
import time
import datetime

from observability_client import get_cloudwatch_logs_client
from observability_models import LogEvent


def write_structured_log(log_group_name: str, log_stream_name: str, event: LogEvent):
    client = get_cloudwatch_logs_client()

    # If timestamp is not provided, use current time in milliseconds
    timestamp = (
        event.timestamp if event.timestamp is not None else int(time.time() * 1000)
    )

    log_entry = {
        "message": event.message,
        "timestamp": timestamp,
    }
    if event.attributes:
        log_entry.update(event.attributes)

    # CloudWatch Logs expects message to be a string
    message_string = json.dumps(log_entry)

    try:
        # Check if log stream exists, create if not
        try:
            client.describe_log_streams(
                logGroupName=log_group_name, logStreamNamePrefix=log_stream_name
            )
        except client.exceptions.ResourceNotFoundException:
            client.create_log_stream(
                logGroupName=log_group_name, logStreamName=log_stream_name
            )

        response = client.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=[
                {"timestamp": timestamp, "message": message_string},
            ],
        )
        print(f"Successfully wrote structured log to CloudWatch: {response}")
    except Exception as e:
        print(f"Error writing structured log to CloudWatch: {e}")


if __name__ == "__main__":
    # Example Usage:
    log_group = os.environ.get("CLOUDWATCH_LOG_GROUP_NAME", "my-application-logs")
    log_stream = os.environ.get("CLOUDWATCH_LOG_STREAM_NAME", "structured-logs")

    sample_event = LogEvent(
        message="User login attempt",
        attributes={
            "user_id": "user-123",
            "status": "success",
            "ip_address": "192.168.1.1",
            "service": "auth-service",
        },
    )
    write_structured_log(log_group, log_stream, sample_event)
