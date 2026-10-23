from observability_client import CloudWatchLogsClient
from observability_models import CorrelatedLog
from datetime import datetime
from typing import List, Dict, Any


def write_correlated_logs(
    log_group_name: str,
    log_stream_name: str,
    correlation_id: str,
    log_messages: List[Dict[str, Any]],
) -> dict:
    """Writes application log events that include a shared request or correlation identifier
    to AWS CloudWatch Logs.

    Args:
        log_group_name: The name of the CloudWatch log group.
        log_stream_name: The name of the CloudWatch log stream.
        correlation_id: The shared identifier for correlated log events.
        log_messages: A list of dictionaries, each containing 'message' and optional 'fields'.

    Returns:
        The response from the CloudWatch Logs API.
    """
    client = CloudWatchLogsClient()
    log_events = []
    for log_data in log_messages:
        correlated_log = CorrelatedLog(
            message=log_data["message"],
            correlation_id=correlation_id,
            timestamp=datetime.utcnow(),
            fields=log_data.get("fields", {}),
        )
        log_events.append(correlated_log.to_aws_cloudwatch_event())

    # CloudWatch Logs expects events to be sorted by timestamp
    log_events.sort(key=lambda x: x["timestamp"])

    response = client.put_log_events(
        log_group_name=log_group_name,
        log_stream_name=log_stream_name,
        log_events=log_events,
    )
    return response
