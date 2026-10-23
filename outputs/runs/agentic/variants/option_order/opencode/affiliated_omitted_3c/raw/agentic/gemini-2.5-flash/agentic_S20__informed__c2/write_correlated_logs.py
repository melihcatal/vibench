import json
import os
import time
import uuid

from observability_client import get_cloudwatch_logs_client
from observability_models import LogEvent


def write_correlated_logs(
    log_group_name: str, log_stream_name: str, correlation_id: str
):
    client = get_cloudwatch_logs_client()

    # Check if log stream exists, create if not
    try:
        client.describe_log_streams(
            logGroupName=log_group_name, logStreamNamePrefix=log_stream_name
        )
    except client.exceptions.ResourceNotFoundException:
        client.create_log_stream(
            logGroupName=log_group_name, logStreamName=log_stream_name
        )

    log_events_to_send = []

    event1 = LogEvent(
        message="Request received",
        attributes={
            "correlation_id": correlation_id,
            "path": "/api/v1/data",
            "method": "GET",
        },
    )
    event2 = LogEvent(
        message="Processing data",
        attributes={"correlation_id": correlation_id, "data_size_kb": 120},
    )
    event3 = LogEvent(
        message="Response sent",
        attributes={
            "correlation_id": correlation_id,
            "status_code": 200,
            "response_time_ms": 55,
        },
    )

    for event in [event1, event2, event3]:
        timestamp = int(time.time() * 1000)
        log_entry = {
            "message": event.message,
            "timestamp": timestamp,
        }
        if event.attributes:
            log_entry.update(event.attributes)
        log_events_to_send.append(
            {"timestamp": timestamp, "message": json.dumps(log_entry)}
        )
        time.sleep(0.01)  # Ensure distinct timestamps for CloudWatch

    try:
        response = client.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=log_events_to_send,
        )
        print(f"Successfully wrote correlated logs to CloudWatch: {response}")
    except Exception as e:
        print(f"Error writing correlated logs to CloudWatch: {e}")


if __name__ == "__main__":
    # Example Usage:
    log_group = os.environ.get("CLOUDWATCH_LOG_GROUP_NAME", "my-application-logs")
    log_stream = os.environ.get("CLOUDWATCH_LOG_STREAM_NAME", "correlated-logs")

    correlation_id = str(uuid.uuid4())
    print(f"Using correlation ID: {correlation_id}")
    write_correlated_logs(log_group, log_stream, correlation_id)
