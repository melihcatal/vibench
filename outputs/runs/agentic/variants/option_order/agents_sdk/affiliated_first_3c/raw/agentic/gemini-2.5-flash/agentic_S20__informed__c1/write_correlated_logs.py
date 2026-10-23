import os
import google.cloud.logging

# Google Cloud project ID
PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")

def write_correlated_logs(log_name: str, correlation_id: str, messages: list[dict]):
    """
    Writes application log events that include a shared request or correlation identifier
    to Google Cloud Logging.
    """
    if not PROJECT_ID:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

    client = google.cloud.logging.Client(project=PROJECT_ID)
    logger = client.logger(log_name)

    for msg_data in messages:
        entry = {
            "message": msg_data["message"],
            "severity": msg_data.get("severity", "INFO"),
            "correlation_id": correlation_id,
            **msg_data.get("extra_fields", {})
        }
        logger.log_struct(entry)
        print(f"Correlated log written to {log_name} with ID {correlation_id}: {entry}")

if __name__ == "__main__":
    # Example usage
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable for authentication
    # Set GOOGLE_CLOUD_PROJECT_ID environment variable
    request_id = "req-abc-123"
    log_messages = [
        {"message": "Request started", "severity": "INFO"},
        {"message": "Processing data for request", "severity": "DEBUG", "extra_fields": {"data_size_kb": 1024}},
        {"message": "Request completed successfully", "severity": "INFO"}
    ]
    write_correlated_logs(
        log_name="my-app-request-logs",
        correlation_id=request_id,
        messages=log_messages
    )
