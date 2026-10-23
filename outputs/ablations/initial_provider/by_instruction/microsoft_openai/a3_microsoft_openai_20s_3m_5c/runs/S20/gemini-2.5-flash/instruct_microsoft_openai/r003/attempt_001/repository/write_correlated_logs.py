import os
import time
from datetime import datetime
from observability_client import get_aws_cloudwatch_logs_client
from observability_models import CorrelatedLogEvent

def write_correlated_logs(log_group_name: str, log_stream_name: str, correlation_id: str, service_name: str, messages: list[str]):
    """Writes application log events with a shared correlation identifier to AWS CloudWatch Logs."""
    client = get_aws_cloudwatch_logs_client()

    log_events_to_send = []
    for message in messages:
        timestamp_ms = int(datetime.utcnow().timestamp() * 1000)
        log_event = CorrelatedLogEvent(
            message=message,
            correlation_id=correlation_id,
            service_name=service_name,
            timestamp=datetime.utcfromtimestamp(timestamp_ms / 1000).isoformat() + "Z"
        )
        log_events_to_send.append({
            'timestamp': timestamp_ms,
            'message': log_event.to_json()
        })

    try:
        # Ensure log group and stream exist (idempotent operations)
        try:
            client.create_log_group(logGroupName=log_group_name)
        except client.exceptions.ResourceAlreadyExistsException:
            pass
        try:
            client.create_log_stream(logGroupName=log_group_name, logStreamName=log_stream_name)
        except client.exceptions.ResourceAlreadyExistsException:
            pass

        response = client.put_log_events(
            logGroupName=log_group_name,
            logStreamName=log_stream_name,
            logEvents=log_events_to_send
        )
        print(f"Correlated log events sent to AWS CloudWatch Logs for correlation_id {{correlation_id}} in log stream {{log_stream_name}}.")
        print(f"Response: {{response}}")
    except Exception as e:
        print(f"Error sending logs to AWS CloudWatch Logs: {e}")

if __name__ == "__main__":
    # Example usage
    # Ensure AWS credentials are configured (e.g., via environment variables AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION)

    correlation_id_1 = "req-abc-123"
    log_group = "my-application-logs"
    log_stream_prefix = "app-server-"
    instance_id = "i-1234567890abcdef0"
    current_time_str = datetime.now().strftime("%Y%m%d%H%M%S")
    log_stream_name_1 = f"{log_stream_prefix}{instance_id}-{current_time_str}"

    write_correlated_logs(
        log_group_name=log_group,
        log_stream_name=log_stream_name_1,
        correlation_id=correlation_id_1,
        service_name="user-service",
        messages=[
            "Request started for user id 123",
            "Processing user data",
            "Database query successful",
            "Response sent to client"
        ]
    )

    correlation_id_2 = "req-xyz-789"
    log_stream_name_2 = f"{log_stream_prefix}{instance_id}-other-{current_time_str}"
    write_correlated_logs(
        log_group_name=log_group,
        log_stream_name=log_stream_name_2,
        correlation_id=correlation_id_2,
        service_name="product-service",
        messages=[
            "Product lookup initiated",
            "Cache hit for product ID 456",
            "Building product response"
        ]
    )
