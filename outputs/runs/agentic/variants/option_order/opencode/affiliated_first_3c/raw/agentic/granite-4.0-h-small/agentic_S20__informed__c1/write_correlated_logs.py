import json
import os
from observability_client import get_logging_client


def write_correlated_logs(correlation_id, logs):
    """Write a batch of correlated log events to Cloud Logging.

    Args:
        correlation_id (str): A shared request or trace ID to group logs.
        logs (list[dict]): List of log payloads, each containing a message and optional metadata.
    """
    client = get_logging_client()
    for log in logs:
        log["request_id"] = correlation_id
        client.logger.log_struct(log)
    client.flush()
