import time
import json
import boto3
from observability_client import get_cloudwatch_logs_client


def write_correlated_logs(
    message: str, severity: str, request_id: str, timestamp: float = None
):
    """
    Write a structured JSON log event that includes a shared correlation identifier to Amazon CloudWatch Logs.

    Parameters
    ----------
    message: str
        The log message text.
    severity: str
        Log severity level (e.g., "ERROR", "INFO").
    request_id: str
        Shared request/correlation identifier that ties related log events together.
    timestamp: float, optional
        Unix epoch timestamp. If omitted, the current time is used.
    """
    log_event = {
        "timestamp": int(timestamp) if timestamp else int(time.time()),
        "message": message,
        "severity": severity,
        "request_id": request_id,
    }
    cloudwatch = get_cloudwatch_logs_client()
    response = cloudwatch.put_log_events(
        logGroupName="my-application-logs",
        logStreamName="correlated-logs",
        logEvents=[
            {"timestamp": log_event["timestamp"], "message": json.dumps(log_event)}
        ],
    )
    return response
