import os
import google.cloud.logging

# Google Cloud project ID
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")

def write_structured_log(log_name: str, message: str, severity: str, extra_fields: dict):
    """
    Writes a structured JSON log event to Google Cloud Logging.
    """
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    client = google.cloud.logging.Client(project=PROJECT_ID)
    logger = client.logger(log_name)

    # Structured log entry
    entry = {
        "message": message,
        "severity": severity,
        **extra_fields
    }

    logger.log_struct(entry)
    print(f"Structured log written to {log_name}: {entry}")

if __name__ == "__main__":
    # Example usage
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable for authentication
    # Set GOOGLE_CLOUD_PROJECT_ID environment variable
    write_structured_log(
        log_name="my-app-logs",
        message="User login attempt",
        severity="INFO",
        extra_fields={
            "user_id": "user-123",
            "ip_address": "192.168.1.1",
            "event_type": "authentication"
        }
    )
