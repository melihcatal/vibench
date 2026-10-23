"""
Writes a single structured JSON log to Google Cloud Logging.
"""
import os
from observability_client import get_logging_client

def write_single_structured_log():
    """
    Writes a structured log entry to Google Cloud Logging.
    """
    # Instantiates a client
    client = get_logging_client()

    # The name of the log to write to
    log_name = os.environ.get("GCP_LOG_NAME", "my-structured-log")
    logger = client.logger(log_name)

    # The data to log
    payload = {
        "message": "User signed up successfully.",
        "user_id": "user-12345",
        "service": "authentication-service",
        "severity": "INFO"
    }

    # Writes the log entry
    logger.log_json(payload)

    print(f"Logged to {log_name}: {payload}")

if __name__ == "__main__":
    # Note: GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT must be set
    write_single_structured_log()
