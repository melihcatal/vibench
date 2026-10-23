import os
import time
from observability_client import CloudWatchLogsClient
from observability_models import LogEvent

def write_structured_log(message: str, severity: str, metadata: dict):
    region_name = os.environ.get("AWS_REGION_NAME", "us-east-1")
    log_group_name = os.environ.get("LOG_GROUP_NAME", "my-application-logs")
    log_stream_name = os.environ.get("LOG_STREAM_NAME", "my-log-stream")

    client = CloudWatchLogsClient(region_name=region_name)

    log_event = LogEvent(
        message=message,
        severity=severity,
        timestamp=int(time.time() * 1000),  # CloudWatch Logs expects timestamp in milliseconds
        metadata=metadata
    )

    print(f"Writing structured log to AWS CloudWatch Logs: group={log_group_name}, stream={log_stream_name}")
    response = client.put_log_event(
        log_group_name=log_group_name,
        log_stream_name=log_stream_name,
        message=log_event.to_json_string(),
        timestamp=log_event.timestamp
    )
    print("Log event written successfully.")
    return response
