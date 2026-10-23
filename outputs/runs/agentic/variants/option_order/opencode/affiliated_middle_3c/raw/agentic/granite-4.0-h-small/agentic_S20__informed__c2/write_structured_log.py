import json
import os
from observability_client import LogClient, LogMessage


def write_structured_log(data: dict) -> None:
    """Write a structured JSON log event to a managed logging service.

    Uses Amazon CloudWatch Logs as the concrete managed logging service.
    Required environment variables:
        AWS_ACCESS_KEY_ID
        AWS_SECRET_ACCESS_KEY
        AWS_REGION (optional, default 'us-east-1')
    """
    client = LogClient()  # boto3 CloudWatch Logs client initialized in helper
    payload = json.dumps(
        {
            "timestamp": data.get("timestamp"),
            "level": data.get("level"),
            "message": data.get("message"),
        }
    )
    client.put_log_events(
        log_group_name="my-app-logs",
        log_stream_name="structured-logs",
        log_events=[{"timestamp": int(data.get("timestamp", 0)), "message": payload}],
    )
