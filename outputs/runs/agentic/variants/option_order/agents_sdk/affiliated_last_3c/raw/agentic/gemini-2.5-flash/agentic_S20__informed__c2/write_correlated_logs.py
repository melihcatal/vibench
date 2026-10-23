import os
import google.cloud.logging
import uuid

def write_correlated_logs(log_name: str, messages: list[str], correlation_id: str = None):
    """Writes application log events that include a shared request or correlation identifier to Google Cloud Logging."""
    client = google.cloud.logging.Client()
    logger = client.logger(log_name)

    if correlation_id is None:
        correlation_id = str(uuid.uuid4())

    for i, message in enumerate(messages):
        log_entry = {
            "message": message,
            "correlation_id": correlation_id,
            "step": i + 1,
            "environment": os.getenv("APP_ENV", "development"),
        }
        logger.log_struct(log_entry, severity="INFO")
    print(f"Logged {len(messages)} correlated messages to {log_name} with correlation ID {correlation_id}")

if __name__ == "__main__":
    # Example usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    request_id = str(uuid.uuid4())
    write_correlated_logs(
        "my-app-request-logs",
        ["Request started", "Processing data", "Sending response"],
        correlation_id=request_id
    )
