import google.cloud.logging
import os
import uuid

def write_correlated_log(message, correlation_id=None, severity="INFO"):
    """
    Writes a structured log event to Google Cloud Logging with an optional correlation identifier.

    Args:
        message (str): The log message.
        correlation_id (str, optional): A shared request or correlation identifier.
                                        If None, a new one will be generated.
        severity (str, optional): The severity of the log entry (e.g., "INFO", "ERROR").
    """
    client = google.cloud.logging.Client()
    logger = client.logger(name="application_logs")

    if correlation_id is None:
        correlation_id = str(uuid.uuid4())

    log_entry = {
        "message": message,
        "correlation_id": correlation_id,
        "service_name": os.getenv("GAE_SERVICE", "default_service"),
        "version_id": os.getenv("GAE_VERSION", "default_version"),
    }

    logger.log_struct(
        log_entry,
        severity=severity
    )

    print(f"Log with correlation_id {correlation_id} and message '{message}' written to Google Cloud Logging.")

if __name__ == "__main__":
    # Example usage:
    # To run this, ensure you have authenticated with Google Cloud and have the GOOGLE_APPLICATION_CREDENTIALS
    # environment variable set, or are running in a GCP environment.

    # Write a log with a new correlation ID
    write_correlated_log("User login successful for user: test_user_1")

    # Write another log with the same correlation ID to correlate events
    shared_correlation_id = str(uuid.uuid4())
    write_correlated_log("Processing order 123 for customer XYZ", correlation_id=shared_correlation_id)
    write_correlated_log("Payment received for order 123", correlation_id=shared_correlation_id)
    write_correlated_log("Order 123 shipped", correlation_id=shared_correlation_id)

    write_correlated_log("An error occurred during data processing.", severity="ERROR")
