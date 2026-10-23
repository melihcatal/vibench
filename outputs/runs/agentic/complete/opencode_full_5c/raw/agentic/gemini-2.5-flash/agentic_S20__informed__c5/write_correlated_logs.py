from observability_client import get_logging_client
from observability_models import CorrelatedLogEntry


def write_correlated_logs(entries: list[CorrelatedLogEntry]):
    """Writes a list of correlated log events to Google Cloud Logging."""
    client = get_logging_client()
    # Using a single logger for all correlated logs for simplicity, or can create multiple based on log_name in payload
    logger = client.logger("application_correlated_logs")

    for entry in entries:
        log_entry_payload = {
            "message": entry.message,
            "correlation_id": entry.correlation_id,
            **entry.json_payload,
        }
        logger.log(
            log_entry_payload,
            severity=entry.severity,
            resource={"type": entry.resource_type, "labels": entry.resource_labels},
        )
        print(
            f"Correlated log written with ID: {entry.correlation_id}, message: {entry.message}"
        )


if __name__ == "__main__":
    # Example usage:
    request_id = "req-abc-123"
    correlated_logs = [
        CorrelatedLogEntry(
            message="Request started",
            correlation_id=request_id,
            severity="INFO",
            json_payload={"path": "/api/v1/data", "method": "GET"},
        ),
        CorrelatedLogEntry(
            message="Processing data",
            correlation_id=request_id,
            severity="DEBUG",
            json_payload={"data_size": 1024, "step": "validation"},
        ),
        CorrelatedLogEntry(
            message="Request completed",
            correlation_id=request_id,
            severity="INFO",
            json_payload={"status_code": 200, "duration_ms": 150},
        ),
    ]
    write_correlated_logs(correlated_logs)

    another_request_id = "req-xyz-456"
    another_correlated_logs = [
        CorrelatedLogEntry(
            message="User creation initiated",
            correlation_id=another_request_id,
            severity="INFO",
            json_payload={"new_user_email": "test@example.com"},
        ),
        CorrelatedLogEntry(
            message="Error sending welcome email",
            correlation_id=another_request_id,
            severity="WARNING",
            json_payload={"email_service_error": "timeout"},
        ),
    ]
    write_correlated_logs(another_correlated_logs)
