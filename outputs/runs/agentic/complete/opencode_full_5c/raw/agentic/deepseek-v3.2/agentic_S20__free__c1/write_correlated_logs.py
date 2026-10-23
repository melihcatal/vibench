import boto3
import json
import os
import uuid
from datetime import datetime
from observability_client import get_cloudwatch_client


def write_correlated_logs(
    log_group_name, log_stream_name, correlation_id=None, log_events=None
):
    """
    Write application log events that include a shared request or correlation identifier.

    Args:
        log_group_name: CloudWatch Logs group name
        log_stream_name: CloudWatch Logs stream name
        correlation_id: Optional correlation ID (generated if not provided)
        log_events: List of log event dictionaries
    """
    client = get_cloudwatch_client()

    # Generate correlation ID if not provided
    if correlation_id is None:
        correlation_id = str(uuid.uuid4())

    if log_events is None:
        log_events = [
            {"message": "Request started", "level": "INFO"},
            {"message": "Processing data", "level": "INFO"},
            {"message": "Request completed", "level": "INFO"},
        ]

    # Add correlation ID and timestamp to each event
    cloudwatch_events = []
    for event in log_events:
        event["correlation_id"] = correlation_id
        event["timestamp"] = int(datetime.now().timestamp() * 1000)

        cloudwatch_event = {
            "timestamp": event["timestamp"],
            "message": json.dumps(event),
        }
        cloudwatch_events.append(cloudwatch_event)

    try:
        # Create log stream if it doesn't exist
        try:
            client.create_log_stream(
                logGroupName=log_group_name, logStreamName=log_stream_name
            )
        except client.exceptions.ResourceAlreadyExistsException:
            pass

        # Put log events
        response = client.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=cloudwatch_events,
        )

        return {
            "success": True,
            "correlation_id": correlation_id,
            "nextSequenceToken": response.get("nextSequenceToken"),
            "event_count": len(cloudwatch_events),
        }
    except Exception as e:
        return {"success": False, "error": str(e), "correlation_id": correlation_id}
