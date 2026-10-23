import os
import datetime
from observability_client import get_logging_client, get_log_name
from observability_models import StructuredLog


def write_log_entry(log_payload: StructuredLog):
    """
    Writes a structured log entry to Google Cloud Logging.
    """
    client = get_logging_client()
    logger = client.logger(get_log_name())

    logger.log_struct(log_payload, severity=log_payload.get("severity", "INFO"))


if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_APPLICATION_CREDENTIALS and optionally GCP_LOG_NAME
    # before running.
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
    else:
        log_entry: StructuredLog = {
            "message": "User signed in successfully.",
            "user_id": "user-12345",
            "severity": "INFO",
            "context": {"ip_address": "192.0.2.1", "user_agent": "MyApp/1.0"},
        }
        write_log_entry(log_entry)
        print("Successfully wrote a structured log.")
