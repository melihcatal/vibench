import json
import os
from observability_client import get_cloudwatch_client


def write_correlated_logs(message: str, severity: str, correlation_id: str):
    """Write correlated application log events to a managed log service."""
    log_entry = {
        "timestamp": int(os.time()),
        "message": message,
        "severity": severity,
        "correlation_id": correlation_id,
    }
    client = get_cloudwatch_client()  # using CloudWatch Logs for the example
    response = client.put_log_events(
        logGroupName=os.getenv("CLOUDWATCH_LOG_GROUP"),
        logStreamName=os.getenv("CLOUDWATCH_LOG_STREAM"),
        logEvents=[
            {"timestamp": log_entry["timestamp"], "message": json.dumps(log_entry)}
        ],
    )
    return response
