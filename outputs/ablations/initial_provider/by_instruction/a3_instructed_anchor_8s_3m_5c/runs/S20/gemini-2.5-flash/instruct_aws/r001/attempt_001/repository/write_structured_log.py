import os
import time
from observability_client import ObservabilityClient
from observability_models import StructuredLogEvent

def write_structured_log(message: str, severity: str, service: str, metadata: dict = None):
    client = ObservabilityClient()
    cloudwatch_logs_client = client.get_client()
    log_group_name = client.get_log_group_name()
    log_stream_name = os.getenv('AWS_LOG_STREAM_NAME', 'structured-logs')

    log_event = StructuredLogEvent(message, severity, service, metadata)
    log_entry_json = log_event.to_json()

    try:
        # Ensure log group exists
        # CloudWatch Logs doesn't automatically create log groups on put_log_events
        # Need to check if log group exists and create if not
        try:
            cloudwatch_logs_client.describe_log_groups(logGroupNamePrefix=log_group_name)
        except cloudwatch_logs_client.exceptions.ResourceNotFoundException:
            cloudwatch_logs_client.create_log_group(logGroupName=log_group_name)

        # Ensure log stream exists
        # CloudWatch Logs doesn't automatically create log streams on put_log_events
        # Need to check if log stream exists and create if not
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

        cloudwatch_logs_client.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=[
                {
                    'timestamp': int(time.time() * 1000),
                    'message': log_entry_json
                },
            ]
        )
        print(f"Successfully wrote structured log to AWS CloudWatch Logs: {log_entry_json}")
    except Exception as e:
        print(f"Error writing structured log to AWS CloudWatch Logs: {e}")

# Example Usage (will not be part of the final file, but for testing purposes)
# if __name__ == "__main__":
#     write_structured_log(
#         message="User login successful",
#         severity="INFO",
#         service="authentication-service",
#         metadata={"user_id": "123", "ip_address": "192.168.1.1"}
#     )
