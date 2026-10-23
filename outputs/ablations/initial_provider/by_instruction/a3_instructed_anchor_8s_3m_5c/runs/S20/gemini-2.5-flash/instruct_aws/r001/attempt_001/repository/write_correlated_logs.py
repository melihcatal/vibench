import os
import time
import uuid
from observability_client import ObservabilityClient
from observability_models import StructuredLogEvent

def write_correlated_logs(request_id: str):
    client = ObservabilityClient()
    cloudwatch_logs_client = client.get_client()
    log_group_name = client.get_log_group_name()
    log_stream_name = os.getenv('AWS_CORRELATED_LOG_STREAM_NAME', 'correlated-logs')

    # Ensure log group exists
    try:
        cloudwatch_logs_client.describe_log_groups(logGroupNamePrefix=log_group_name)
    except cloudwatch_logs_client.exceptions.ResourceNotFoundException:
        cloudwatch_logs_client.create_log_group(logGroupName=log_group_name)

    # Ensure log stream exists
    try:
        cloudwatch_logs_client.describe_log_streams(
            logGroupName=log_group_name,
            logStreamNamePrefix=log_stream_name
        )
    except cloudwatch_logs_client.exceptions.ResourceNotFoundException:
        cloudwatch_logs_client.create_log_stream(
            logGroupName=log_group_name,
            logStreamName=log_stream_name
        )

    log_events = [
        StructuredLogEvent(
            message="Request received",
            severity="INFO",
            service="api-gateway",
            correlation_id=request_id,
            metadata={"path": "/users", "method": "GET"}
        ),
        StructuredLogEvent(
            message="Processing user data",
            severity="INFO",
            service="user-service",
            correlation_id=request_id,
            metadata={"user_id": "123"}
        ),
        StructuredLogEvent(
            message="Database query successful",
            severity="DEBUG",
            service="user-service",
            correlation_id=request_id,
            metadata={"query_time_ms": 50}
        )
    ]

    entries = []
    for event in log_events:
        entries.append({
            'timestamp': int(time.time() * 1000),
            'message': event.to_json()
        })

    try:
        cloudwatch_logs_client.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=entries
        )
        print(f"Successfully wrote {len(log_events)} correlated logs with request_id {request_id} to AWS CloudWatch Logs")
    except Exception as e:
        print(f"Error writing correlated logs to AWS CloudWatch Logs: {e}")

# Example Usage (will not be part of the final file)
# if __name__ == "__main__":
#     correlation_id = str(uuid.uuid4())
#     write_correlated_logs(correlation_id)
