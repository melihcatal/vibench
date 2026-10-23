import time
import json
import boto3
from observability_client import get_cloudwatch_logs_client


def write_structured_log(
    message: str, severity: str, request_id: str = None, timestamp: float = None
):
    """
    Write a structured JSON log event to Amazon CloudWatch Logs.

    Parameters
    ----------
    message: str
        The log message text.
    severity: str
        Log severity level (e.g., "ERROR", "INFO").
    request_id: str, optional
        Correlation identifier to include in the log.
    timestamp: float, optional
        Unix epoch timestamp. If omitted, the current time is used.
    """
    log_event = {
        "timestamp": int(timestamp) if timestamp else int(time.time()),
        "message": message,
        "severity": severity,
    }
    if request_id:
        log_event["request_id"] = request_id

    cloudwatch = get_cloudwatch_logs_client()
    response = cloudwatch.put_log_events(
        logGroupName="my-application-logs",
        logStreamName="structured-logs",
        logEvents=[
            {"timestamp": log_event["timestamp"], "message": json.dumps(log_event)}
        ],
    )
    return response
