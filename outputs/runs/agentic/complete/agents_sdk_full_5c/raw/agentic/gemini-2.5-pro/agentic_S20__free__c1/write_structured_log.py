from google.cloud import logging
import os

from observability_client import get_gcp_logging_client
from observability_models import StructuredLog


def write_log_entry(log_payload: StructuredLog):
    """Writes a structured log entry to Google Cloud Logging.

    Args:
        log_payload: A StructuredLog object representing the log entry.
    """
    logging_client = get_gcp_logging_client()
    
    # The name of the log to write to
    log_name = "my-structured-log"
    logger = logging_client.logger(log_name)

    # The data to log
    data = log_payload.model_dump()

    # Writes the log entry
    logger.log_struct(data, severity=log_payload.severity)

    print(f"Logged: {data} to {log_name}")


# Example of a structured log event for a user action
user_action_log = StructuredLog(
    message="User signed in successfully",
    user_id="user_12345",
    service_name="auth-service",
    request_method="POST",
    request_url="/api/login",
    response_status_code=200,
    severity="INFO"
)
# To run this, you would call write_log_entry(user_action_log)
