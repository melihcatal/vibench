import json
from observability_client import get_logger
from observability_models import StructuredLog

def write_log_event(log_data: StructuredLog):
    """
    Writes a single structured log entry to Google Cloud Logging.

    Args:
        log_data (StructuredLog): The structured log data to write.
    """
    logger = get_logger("structured_log_writer")

    payload = {
        "message": log_data.message,
        "service": log_data.service_context,
        "request_id": log_data.request_id,
        "user_id": log_data.user_id,
        "custom_data": log_data.extra_data,
        "timestamp": log_data.timestamp,
    }
    
    # Use log_struct to send a structured JSON payload
    logger.log_struct(payload, severity=log_data.severity)

    print(f"Successfully sent structured log with severity {log_data.severity}.")


if __name__ == '__main__':
    # Example of writing a structured log
    log_event = StructuredLog(
        message="User successfully logged in.",
        request_id="req-abc-123",
        user_id="user-456",
        service_context="auth-service",
        severity="INFO",
        extra_data={"login_method": "password", "ip_address": "192.0.2.1"}
    )
    write_log_event(log_event)

    error_event = StructuredLog(
        message="Failed to connect to database.",
        request_id="req-def-456",
        service_context="database-connector",
        severity="ERROR",
        extra_data={"db_host": "db.example.com", "retry_attempts": 3}
    )
    write_log_event(error_event)
