import os
import datetime
import uuid
from google.cloud import logging

def write_correlated_logs(request_id: str, messages: list[dict]):
    """Writes multiple application log events that include a shared request identifier to Google Cloud Logging."""
    client = logging.Client()
    logger = client.logger(name="correlated_application_logs")

    for msg in messages:
        log_entry = {
            "requestId": request_id,
            "message": msg.get("message", "No message provided"),
            "severity": msg.get("severity", "INFO"),
            "component": msg.get("component", "unknown_component"),
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        }
        logger.log_struct(log_entry, severity=log_entry["severity"])
        print(f"Logged correlated message for request {request_id}: {log_entry['message']}")

if __name__ == "__main__":
    # Example usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    correlation_id = str(uuid.uuid4())
    print(f"Using correlation ID: {correlation_id}")
    log_events = [
        {"message": "Starting user request processing.", "severity": "INFO", "component": "web_frontend"},
        {"message": "Fetching user profile from database.", "severity": "DEBUG", "component": "user_service"},
        {"message": "Successfully processed user request.", "severity": "INFO", "component": "web_frontend"},
    ]
    write_correlated_logs(correlation_id, log_events)

    error_correlation_id = str(uuid.uuid4())
    print(f"Using correlation ID: {error_correlation_id}")
    error_log_events = [
        {"message": "Received malformed request.", "severity": "WARNING", "component": "api_gateway"},
        {"message": "Failed to parse request body.", "severity": "ERROR", "component": "api_gateway"},
    ]
    write_correlated_logs(error_correlation_id, error_log_events)
