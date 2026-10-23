from observability_client import get_logging_client
from observability_models import create_log_entry
import os

PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
LOG_NAME = "my-structured-app-log"

def write_structured_log(log_message: str, data: dict, severity: str = 'INFO'):
    """Writes a structured JSON log event to Google Cloud Logging.

    Args:
        log_message: The main message for the log entry.
        data: A dictionary of additional structured data.
        severity: The severity of the log entry (e.g., 'INFO', 'ERROR').
    """
    client = get_logging_client()
    logger = client.logger(LOG_NAME)

    # Combine message and data into a single structured payload
    log_payload = create_log_entry(message=log_message, severity=severity, **data)

    logger.log_struct(log_payload, severity=severity)
    print(f"Wrote structured log to Google Cloud Logging: {log_payload}")

if __name__ == '__main__':
    # Example usage
    write_structured_log(
        log_message="User login attempt",
        data={
            "user_id": "user-123",
            "ip_address": "192.168.1.1",
            "status": "success"
        },
        severity="INFO"
    )
