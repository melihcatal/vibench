import os
import json
from observability_client import get_cloudwatch_logs_client

def write_correlated_logs(message: str, correlation_id: str, level: str = "INFO", service: str = "my_service") -> None:
    """Write one or more structured log events that share a correlation identifier to CloudWatch Logs.
    Args:
        message: Log payload (can include details per event).
        correlation_id: Shared request/trace ID to correlate across logs.
        level: Log level such as INFO, ERROR, DEBUG.
        service: Logical service name for contextual logging.
    """
    log_entry = {
        "timestamp": int(1000 * os.getenv("SOURCE_TIMESTAMP_MS", 0)),
        "correlationId": correlation_id,
        "level": level,
        "service": service,
        "message": message,
    }
    client = get_cloudwatch_logs_client()
    log_group = "/aws/myapp/correlated-logs"
    log_stream = "correlated-stream"
    client.put_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        logEvents=[{"timestamp": int(1000 * os.getenv("SOURCE_TIMESTAMP_MS", 0)), "message": json.dumps(log_entry)}]
    )
    print(f"Correlated log sent. Event={log_entry}")
