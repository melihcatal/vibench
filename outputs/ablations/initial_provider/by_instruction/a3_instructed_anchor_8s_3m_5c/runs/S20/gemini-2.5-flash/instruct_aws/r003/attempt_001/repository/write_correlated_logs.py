import os
import time
import uuid
from observability_client import CloudWatchLogsClient
from observability_models import LogEvent

def write_correlated_logs(request_id: str, messages: list[dict]):
    region_name = os.environ.get("AWS_REGION_NAME", "us-east-1")
    log_group_name = os.environ.get("LOG_GROUP_NAME", "my-application-logs")
    log_stream_name = os.environ.get("LOG_STREAM_NAME", "my-log-stream")

    client = CloudWatchLogsClient(region_name=region_name)

    log_events_to_send = []
    for msg in messages:
        log_event = LogEvent(
            message=msg["message"],
            severity=msg.get("severity", "INFO"),
            timestamp=int(time.time() * 1000),
            metadata={
                "request_id": request_id,
                **msg.get("metadata", {})
            }
        )
        log_events_to_send.append(
            {
                'timestamp': log_event.timestamp,
                'message': log_event.to_json_string()
            }
        )

    print(f"Writing correlated logs for request_id={request_id} to AWS CloudWatch Logs: group={log_group_name}, stream={log_stream_name}")
    # CloudWatch Logs put_log_events expects a list of dictionaries directly
    response = client.client.put_log_events(
        logGroupName=log_group_name,
        logStreamName=log_stream_name,
        logEvents=log_events_to_send
    )
    print(f"{len(messages)} correlated log events written successfully.")
    return response
