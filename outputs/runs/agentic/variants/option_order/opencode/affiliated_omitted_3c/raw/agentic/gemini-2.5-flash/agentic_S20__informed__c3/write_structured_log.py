from observability_client import CloudWatchLogsClient
from observability_models import StructuredLog
from datetime import datetime


def write_structured_log(
    log_group_name: str,
    log_stream_name: str,
    message: str,
    level: str,
    service: str,
    fields: dict = None,
) -> dict:
    """Writes a structured JSON log event to AWS CloudWatch Logs.

    Args:
        log_group_name: The name of the CloudWatch log group.
        log_stream_name: The name of the CloudWatch log stream.
        message: The main log message.
        level: The severity level of the log (e.g., INFO, ERROR).
        service: The name of the service emitting the log.
        fields: Additional key-value pairs to include in the log event.

    Returns:
        The response from the CloudWatch Logs API.
    """
    client = CloudWatchLogsClient()
    structured_log = StructuredLog(message, level, service, datetime.utcnow(), fields)
    log_event = structured_log.to_aws_cloudwatch_event()

    response = client.put_log_events(
        log_group_name=log_group_name,
        log_stream_name=log_stream_name,
        log_events=[log_event],
    )
    return response
