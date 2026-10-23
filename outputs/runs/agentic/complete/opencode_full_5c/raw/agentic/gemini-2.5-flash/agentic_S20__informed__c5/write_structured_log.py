from observability_client import get_logging_client
from observability_models import StructuredLogEntry


def write_structured_log(entry: StructuredLogEntry):
    """Writes a structured JSON log event to Google Cloud Logging."""
    client = get_logging_client()
    logger = client.logger(entry.json_payload.get("log_name", "application_log"))

    # Google Cloud Logging automatically structures JSON payloads
    # severity and timestamp are typically part of the log entry metadata
    # but can also be explicitly set if needed.
    log_entry_payload = {"message": entry.message, **entry.json_payload}

    logger.log(
        log_entry_payload,
        severity=entry.severity,
        resource={"type": entry.resource_type, "labels": entry.resource_labels},
    )
    print(f"Structured log written successfully with severity: {entry.severity}")


if __name__ == "__main__":
    # Example usage:
    log_entry = StructuredLogEntry(
        message="User login successful",
        severity="INFO",
        json_payload={
            "user_id": "user-123",
            "ip_address": "192.168.1.1",
            "event_type": "authentication",
        },
    )
    write_structured_log(log_entry)

    error_log_entry = StructuredLogEntry(
        message="Database connection failed",
        severity="ERROR",
        json_payload={
            "database": "production_db",
            "error_code": 500,
            "log_name": "database_errors",
        },
    )
    write_structured_log(error_log_entry)
