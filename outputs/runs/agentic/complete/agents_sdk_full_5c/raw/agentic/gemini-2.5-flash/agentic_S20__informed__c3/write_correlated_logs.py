import os
import uuid
import datetime
from google.cloud import logging

def write_correlated_logs(log_name: str, correlation_id: str, messages: list[dict]):
    """
    Writes multiple application log events with a shared correlation identifier to Google Cloud Logging.
    Each message dict should contain at least 'message' and optionally 'severity' and other fields.
    """
    client = logging.Client()
    logger = client.logger(log_name)

    entries = []
    for msg_data in messages:
        message = msg_data.pop("message", "No message provided")
        severity = msg_data.pop("severity", "INFO").upper()

        log_entry = {
            "message": message,
            "severity": severity,
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "correlationId": correlation_id,
            **msg_data,
        }
        entries.append(logging.Client.struct(log_entry, severity=severity))

    logger.write(entries)
    print(f"Correlated logs written to {log_name} with correlation ID: {correlation_id}")
    for entry in entries:
        print(f"  - {entry['jsonPayload']['message']} (Severity: {entry['severity']})")

if __name__ == "__main__":
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT") # Ensure GOOGLE_APPLICATION_CREDENTIALS is set
    if not project_id:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
        exit(1)

    log_name = "my-correlated-app-log"
    request_id = str(uuid.uuid4())

    log_messages = [
        {"message": "Request received", "component": "web-server"},
        {"message": "Processing user data", "component": "data-processor", "user": "test_user"},
        {"message": "Database query executed", "component": "database", "query": "SELECT * FROM users"},
        {"message": "Response sent", "component": "web-server", "status": 200},
    ]

    write_correlated_logs(log_name, request_id, log_messages)

    print("\n--- Another correlated event ---")
    another_request_id = str(uuid.uuid4())
    error_messages = [
        {"message": "User session expired", "severity": "WARNING", "user": "guest"},
        {"message": "Failed to update profile", "severity": "ERROR", "user": "guest", "reason": "invalid_data"},
    ]
    write_correlated_logs(log_name, another_request_id, error_messages)
