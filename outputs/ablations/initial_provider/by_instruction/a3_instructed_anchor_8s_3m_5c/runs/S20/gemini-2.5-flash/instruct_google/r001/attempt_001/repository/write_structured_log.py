from google.cloud import logging

def write_structured_log(log_name: str, message: dict, severity: str = "INFO"):
    """
    Writes a structured JSON log event to Google Cloud Logging.

    Args:
        log_name: The name of the log to write to (e.g., "my-application-log").
        message: A dictionary representing the structured JSON payload.
        severity: The severity of the log entry (e.g., "INFO", "ERROR", "DEBUG").
    """
    client = logging.Client()
    logger = client.logger(log_name)
    logger.log(json_payload=message, severity=severity)

if __name__ == "__main__":
    # Example usage:
    log_name = "my-app-logs"
    structured_data = {
        "event_type": "user_action",
        "user_id": "12345",
        "action": "login",
        "ip_address": "192.168.1.1",
        "details": {"session_id": "abc-123", "device": "mobile"}
    }
    write_structured_log(log_name, structured_data, severity="INFO")

    error_data = {
        "event_type": "application_error",
        "service": "authentication-service",
        "error_code": "AUTH-001",
        "message": "Failed to connect to user database.",
        "trace_id": "trace-xyz-789"
    }
    write_structured_log(log_name, error_data, severity="ERROR")
