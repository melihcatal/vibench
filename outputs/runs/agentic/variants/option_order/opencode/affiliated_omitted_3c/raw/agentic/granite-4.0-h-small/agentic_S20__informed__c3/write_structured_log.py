import json
import os

time
from observability_client import get_log_client


def write_structured_log(message: str, severity: str, request_id: str) -> None:
    """Writes a JSON log event with request correlation to the selected managed logging service.

    The concrete provider used here is Amazon CloudWatch Logs via boto3.
    """
    client = get_log_client()  # boto3 CloudWatch Logs client configured via env vars
    log_event = {
        "timestamp": int,  # will be set by CloudWatch Logs to ingestion time
        "message": message,
        "severity": severity,
        "requestId": request_id,
    }
    # Send the JSON payload
    response = client.put_log_events(
        logGroupName=os.getenv("CLOUDWATCH_LOG_GROUP"),
        logStreamName=os.getenv("CLOUDWATCH_LOG_STREAM"),
        logEvents=[
            {
                "timestamp": int(round(time.time() * 1000)),
                "message": json.dumps(log_event),
            }
        ],
    )
    # Simple check – raise if non‑OK
    if response.get("rejectedLogEventsInfo"):
        raise RuntimeError(f"Failed to write log: {response}")
