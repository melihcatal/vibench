import datetime
from observability_client import get_logging_client, get_project_id
from observability_models import LogEntry

def write_structured_log(log_name: str, message: str, severity: str = "INFO", labels: dict = None, json_payload: dict = None):
    """Writes a structured JSON log event to Google Cloud Logging."""
    client = get_logging_client()
    logger = client.logger(log_name)

    # Google Cloud Logging expects json_payload directly if it's structured
    # rather than passing it as a 'message'.
    # The 'message' part usually goes into a 'textPayload' or part of jsonPayload if structured.
    # For a truly structured log, we'll put the primary message inside json_payload.

    payload = {"message": message, "timestamp": datetime.datetime.utcnow().isoformat() + "Z"}
    if json_payload:
        payload.update(json_payload)

    logger.log_struct(payload, severity=severity, labels=labels)
    print(f"Wrote structured log to {log_name} with severity {severity}")

if __name__ == "__main__":
    project_id = get_project_id()
    log_name = "my-app-logs"
    write_structured_log(
        log_name,
        message="User login attempt",
        severity="INFO",
        labels={"component": "authentication", "user_id": "testuser123"},
        json_payload={"event_type": "login", "status": "success", "ip_address": "192.168.1.1"}
    )

    write_structured_log(
        log_name,
        message="Failed to connect to database",
        severity="ERROR",
        labels={"component": "database", "error_code": "DB-001"},
        json_payload={"exception": "ConnectionRefusedError", "details": "Could not reach db-server:5432"}
    )
