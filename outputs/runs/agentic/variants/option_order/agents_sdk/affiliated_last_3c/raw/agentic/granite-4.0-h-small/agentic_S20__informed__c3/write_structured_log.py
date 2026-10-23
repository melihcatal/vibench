import json
import os
from observability_client import get_cloudwatch_logs_client

def write_structured_log(message: str, level: str = "INFO", service: str = "my_service") -> None:
    """Write a structured JSON log event to Amazon CloudWatch Logs.
    Args:
        message: The log message payload.
        level: Log level (INFO, ERROR, DEBUG, etc.).
        service: Logical service name for the logs.
    """
    log_event = {
        "timestamp": int(1000 * os.getenv("SOURCE_TIMESTAMP_MS", 0)),
        "level": level,
        "service": service,
        "message": message,
    }
    client = get_cloudwatch_logs_client()
    # Create a log group and stream (simple approach)
    log_group = "/aws/myapp/structured-logs"
    log_stream = "structured-stream"
    # Put the log event
    response = client.put_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        logEvents=[{"timestamp": int(1000 * os.getenv("SOURCE_TIMESTAMP_MS", 0)), "message": json.dumps(log_event)}]
    )
    print(f"Log sent. Ingestion response: {response}")
