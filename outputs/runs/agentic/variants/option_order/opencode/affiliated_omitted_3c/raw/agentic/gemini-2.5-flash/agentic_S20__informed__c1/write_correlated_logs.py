from observability_client import ObservabilityClient
from observability_models import CorrelatedLogEvent
import os
import time


def write_correlated_logs(
    correlation_id: str, messages: list[str], log_group_name: str, log_stream_name: str
):
    client = ObservabilityClient()

    print(
        f"Writing correlated logs for correlation_id='{correlation_id}' to {log_group_name}/{log_stream_name}:"
    )

    # Ensure log group and stream exist
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

    log_events = []
    for msg in messages:
        log_event = CorrelatedLogEvent(correlation_id=correlation_id, message=msg)
        log_events.append(log_event.to_cloudwatch_event())
        print(f"  - {log_event.message}")
        time.sleep(0.001)  # Ensure unique timestamps if generated quickly

    response = client.put_log_events(
        log_group_name=log_group_name,
        log_stream_name=log_stream_name,
        log_events=log_events,
    )
    print(
        f"Correlated log events written successfully for correlation_id='{correlation_id}'."
    )
    return response


if __name__ == "__main__":
    # Example usage: Ensure AWS_REGION environment variable is set
    # Example: export AWS_REGION=us-east-1
    log_group = os.environ.get("CLOUDWATCH_LOG_GROUP", "my-application-logs")
    log_stream = os.environ.get("CLOUDWATCH_LOG_STREAM", "correlated-logs")

    request_id_1 = "req-abc-123"
    correlated_messages_1 = [
        "Request received for /api/v1/data",
        "Authenticating user session",
        "Fetching data from database",
        "Data retrieval successful, returning response",
    ]
    write_correlated_logs(request_id_1, correlated_messages_1, log_group, log_stream)

    time.sleep(1)  # Separate batches for clarity in logs

    request_id_2 = "req-xyz-456"
    correlated_messages_2 = [
        "Request received for /api/v1/update",
        "User not authorized for update operation",
        "Returning 403 Forbidden",
    ]
    write_correlated_logs(request_id_2, correlated_messages_2, log_group, log_stream)
