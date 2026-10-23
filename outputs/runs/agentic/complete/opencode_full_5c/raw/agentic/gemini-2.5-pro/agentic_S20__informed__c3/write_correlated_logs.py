import os
import uuid
from observability_client import ObservabilityClient
from observability_models import LogEntry


def write_correlated_logs():
    """
    Writes multiple log events with a shared correlation ID to Google Cloud Logging.
    """
    client = ObservabilityClient()
    logger_name = os.getenv("GCP_LOG_NAME", "my-correlated-log")
    correlation_id = str(uuid.uuid4())

    log_entry_1 = LogEntry(
        message="Starting payment processing.",
        severity="INFO",
        request_id=correlation_id,
        extra_data={"step": "start", "service": "payment-service"},
    )
    client.write_log_entry(logger_name, log_entry_1)
    print(f"Wrote log 1 for correlation ID {correlation_id}")

    log_entry_2 = LogEntry(
        message="Contacting banking partner.",
        severity="DEBUG",
        request_id=correlation_id,
        extra_data={"step": "contact_bank", "service": "payment-service"},
    )
    client.write_log_entry(logger_name, log_entry_2)
    print(f"Wrote log 2 for correlation ID {correlation_id}")

    log_entry_3 = LogEntry(
        message="Payment processed successfully.",
        severity="INFO",
        request_id=correlation_id,
        extra_data={"step": "finish", "service": "payment-service"},
    )
    client.write_log_entry(logger_name, log_entry_3)
    print(f"Wrote log 3 for correlation ID {correlation_id}")


if __name__ == "__main__":
    write_correlated_logs()
