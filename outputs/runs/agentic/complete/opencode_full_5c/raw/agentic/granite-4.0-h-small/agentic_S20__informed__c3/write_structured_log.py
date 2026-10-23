import json
import os
from observability_client import get_cloudwatch_client


def write_structured_log(message: str, severity: str, request_id: str):
    """Write a structured JSON log event to Amazon CloudWatch Logs."""
    log_event = {
        "timestamp": int(os.time()),
        "message": message,
        "severity": severity,
        "request_id": request_id,
    }
    client = get_cloudwatch_client()
    response = client.put_log_events(
        logGroupName=os.getenv("CLOUDWATCH_LOG_GROUP"),
        logStreamName=os.getenv("CLOUDWATCH_LOG_STREAM"),
        logEvents=[
            {"timestamp": log_event["timestamp"], "message": json.dumps(log_event)}
        ],
    )
    return response
