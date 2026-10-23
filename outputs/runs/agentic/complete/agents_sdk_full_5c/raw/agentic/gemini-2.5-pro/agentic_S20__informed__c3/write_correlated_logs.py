"""
Writes multiple log events with a shared correlation ID.
"""
import os
import uuid
from observability_client import get_logging_client

def write_app_correlated_logs():
    """
    Writes a series of application logs with a common correlation ID
    to Google Cloud Logging.
    """
    client = get_logging_client()
    log_name = os.environ.get("GCP_LOG_NAME", "my-correlated-log")
    logger = client.logger(log_name)

    correlation_id = str(uuid.uuid4())

    # First log: request received
    log_1 = {
        "message": "Request received for order processing.",
        "correlation_id": correlation_id,
        "service": "api-gateway",
        "severity": "INFO",
        "step": "1_received"
    }
    logger.log_json(log_1)
    print(f"Logged event 1 for correlation ID {correlation_id}")

    # Second log: processing started
    log_2 = {
        "message": "Beginning payment authorization.",
        "correlation_id": correlation_id,
        "service": "payment-service",
        "severity": "INFO",
        "step": "2_payment_auth"
    }
    logger.log_json(log_2)
    print(f"Logged event 2 for correlation ID {correlation_id}")

    # Third log: processing failed
    log_3 = {
        "message": "Payment authorization failed: Insufficient funds.",
        "correlation_id": correlation_id,
        "service": "payment-service",
        "severity": "ERROR",
        "step": "3_payment_failed"
    }
    logger.log_json(log_3)
    print(f"Logged event 3 for correlation ID {correlation_id}")


if __name__ == "__main__":
    # Note: GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT must be set
    write_app_correlated_logs()
