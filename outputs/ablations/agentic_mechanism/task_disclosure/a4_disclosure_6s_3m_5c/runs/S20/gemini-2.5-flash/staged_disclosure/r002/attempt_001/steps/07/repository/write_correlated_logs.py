
import os
import uuid
import logging
from google.cloud import logging as cloud_logging

# Initialize Google Cloud Logging client
# Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set or
# running in a Google Cloud environment with appropriate permissions.
try:
    client = cloud_logging.Client()
    logger = client.logger('application_logs')
except Exception as e:
    print(f"Could not initialize Google Cloud Logging client: {e}")
    print("Please ensure GOOGLE_APPLICATION_CREDENTIALS is set or you are running in a GCP environment.")
    # Fallback to basic logging if Cloud Logging client fails to initialize
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('application_logs')


def write_correlated_log_events(message: str, severity: str = "INFO", correlation_id: str = None):
    """
    Writes an application log event with an optional correlation ID to Google Cloud Logging.

    Args:
        message (str): The main log message.
        severity (str): The severity of the log event (e.g., "INFO", "WARNING", "ERROR").
        correlation_id (str): An optional correlation ID to link related log events.
                              If not provided, a new one will be generated for this event.
    """
    if correlation_id is None:
        correlation_id = str(uuid.uuid4())

    log_entry = {
        "message": message,
        "severity": severity,
        "jsonPayload": {
            "correlation_id": correlation_id,
        }
    }

    if isinstance(logger, cloud_logging.Logger):
        logger.log_struct(log_entry)
        print(f"Cloud Logging: [{severity}] [Correlation ID: {correlation_id}] {message}")
    else:
        # Fallback logging
        if severity == "INFO":
            logger.info(f"[Correlation ID: {correlation_id}] {message}")
        elif severity == "WARNING":
            logger.warning(f"[Correlation ID: {correlation_id}] {message}")
        elif severity == "ERROR":
            logger.error(f"[Correlation ID: {correlation_id}] {message}")
        else:
            logger.info(f"[Correlation ID: {correlation_id}] {message}")
        print(f"Basic Logging: [{severity}] [Correlation ID: {correlation_id}] {message}")

if __name__ == "__main__":
    # Example Usage:

    # Simulate a single request with a shared correlation ID
    request_id_1 = str(uuid.uuid4())
    print(f"Simulating request with Correlation ID: {request_id_1}")
    write_correlated_log_events("User initiated login.", "INFO", request_id_1)
    write_correlated_log_events("Authentication successful.", "INFO", request_id_1)
    write_correlated_log_events("User profile loaded.", "INFO", request_id_1)
    write_correlated_log_events("Possible suspicious activity detected.", "WARNING", request_id_1)

    print("\nSimulating another request with a different Correlation ID:")
    request_id_2 = str(uuid.uuid4())
    write_correlated_log_events("Product search initiated.", "INFO", request_id_2)
    write_correlated_log_events("Database query failed.", "ERROR", request_id_2)
    write_correlated_log_events("Fallback search results displayed.", "INFO", request_id_2)

    print("\nSimulating a log event without explicitly providing a Correlation ID:")
    write_correlated_log_events("Background job started.")
    write_correlated_log_events("Background job completed successfully.")
