from google.cloud import logging
import os
from datetime import datetime

# Initialize Google Cloud Logging client
client = logging.Client.from_service_account_json(
    os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
)
logger = client.logger("correlated_application_logs")


def write_correlated_logs(correlation_id: str, log_events: list[dict]) -> None:
    """
    Writes application log events with a shared correlation identifier to Google Cloud Logging.

    Args:
        correlation_id (str): The shared request or correlation identifier.
        log_events (list[dict]): List of log events to write.
    """
    if not isinstance(log_events, list):
        raise ValueError("log_events must be a list of dictionaries")

    for event in log_events:
        if not isinstance(event, dict):
            raise ValueError("Each log event must be a dictionary")

        # Add correlation_id and timestamp if not provided
        event["correlation_id"] = correlation_id
        if "timestamp" not in event:
            event["timestamp"] = datetime.utcnow().isoformat()

        # Write the log entry
        logger.log_struct(
            event,
            severity=event.get("severity", "INFO"),
            resource=logging.Resource(type="global"),
        )
