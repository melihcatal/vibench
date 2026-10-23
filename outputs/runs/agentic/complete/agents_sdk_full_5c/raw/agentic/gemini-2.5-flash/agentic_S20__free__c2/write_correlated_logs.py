from google.cloud import logging
import os
import uuid
import json

def write_correlated_logs(log_name: str, request_id: str, messages: list):
    """Writes multiple log entries with a shared request ID to Google Cloud Logging."""
    client = logging.Client()
    logger = client.logger(log_name)

    for i, message_data in enumerate(messages):
        log_entry = {
            "message": message_data.get("message"),
            "severity": message_data.get("severity", "INFO"),
            "component": message_data.get("component", "unknown"),
            "request_id": request_id,
            "sequence_num": i + 1
        }
        logger.log_struct(
            log_entry,
            severity=log_entry["severity"],
            labels={"correlation_id": request_id, "environment": os.getenv("APP_ENV", "development")}
        )
        print(f"Correlated log written to {log_name} (req_id={request_id}): {json.dumps(log_entry)}")

if __name__ == "__main__":
    PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not PROJECT_ID:
        print("GOOGLE_CLOUD_PROJECT environment variable not set. Please set it to your GCP project ID.")
    else:
        correlation_id = str(uuid.uuid4())
        print(f"Writing logs with correlation ID: {correlation_id}")
        logs_to_write = [
            {"message": "Incoming request processed by gateway", "severity": "INFO", "component": "gateway"},
            {"message": "User data fetched from database", "severity": "INFO", "component": "user-service"},
            {"message": "Response sent to client", "severity": "INFO", "component": "gateway"}
        ]
        write_correlated_logs(
            log_name="my-app-request-logs",
            request_id=correlation_id,
            messages=logs_to_write
        )

        correlation_id_error = str(uuid.uuid4())
        print(f"Writing logs with correlation ID: {correlation_id_error}")
        error_logs_to_write = [
            {"message": "Payment processing started", "severity": "INFO", "component": "payment-service"},
            {"message": "External API timeout", "severity": "ERROR", "component": "payment-service"},
            {"message": "Transaction failed due to external error", "severity": "ERROR", "component": "payment-service"}
        ]
        write_correlated_logs(
            log_name="my-app-request-logs",
            request_id=correlation_id_error,
            messages=error_logs_to_write
        )
