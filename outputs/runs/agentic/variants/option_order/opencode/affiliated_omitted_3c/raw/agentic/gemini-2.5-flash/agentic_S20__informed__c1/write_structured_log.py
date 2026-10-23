from observability_client import ObservabilityClient
from observability_models import StructuredLogEvent
import os


def write_structured_log(
    level: str, service: str, message: str, log_group_name: str, log_stream_name: str
):
    client = ObservabilityClient()
    log_event = StructuredLogEvent(level=level, service=service, message=message)

    print(f"Writing structured log to {log_group_name}/{log_stream_name}:")
    print(log_event.message)

    # Ensure log group and stream exist (CloudWatch Logs requires them)
    # In a real application, you might have a setup script or a more robust mechanism
    try:
        client.cloudwatch_logs_client.create_log_group(logGroupName=log_group_name)
    except client.cloudwatch_logs_client.exceptions.ResourceAlreadyExistsException:
        pass
    try:
        client.cloudwatch_logs_client.create_log_stream(
            logGroupName=log_group_name, logStreamName=log_stream_name
        )
    except client.cloudwatch_logs_client.exceptions.ResourceAlreadyExistsException:
        pass

    response = client.put_log_events(
        log_group_name=log_group_name,
        log_stream_name=log_stream_name,
        log_events=[log_event.to_cloudwatch_event()],
    )
    print("Log event written successfully.")
    return response


if __name__ == "__main__":
    # Example usage: Ensure AWS_REGION environment variable is set
    # Example: export AWS_REGION=us-east-1
    log_group = os.environ.get("CLOUDWATCH_LOG_GROUP", "my-application-logs")
    log_stream = os.environ.get("CLOUDWATCH_LOG_STREAM", "structured-logs")

    write_structured_log(
        level="INFO",
        service="user-auth",
        message="User 'johndoe' logged in successfully.",
        log_group_name=log_group,
        log_stream_name=log_stream,
    )

    write_structured_log(
        level="ERROR",
        service="payment-gateway",
        message="Failed to process payment for order ABC-123. Reason: Insufficient funds.",
        log_group_name=log_group,
        log_stream_name=log_stream,
    )
