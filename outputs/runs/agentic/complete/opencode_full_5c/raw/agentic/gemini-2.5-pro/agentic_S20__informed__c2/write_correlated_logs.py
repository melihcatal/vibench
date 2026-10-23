import os
import uuid
from observability_client import get_logging_client, get_log_name
from observability_models import StructuredLog


def write_correlated_log_entries(
    correlation_id: str, log_payloads: list[StructuredLog]
):
    """
    Writes multiple structured log entries with a shared correlation ID
    to Google Cloud Logging.
    """
    client = get_logging_client()
    logger = client.logger(get_log_name())

    for payload in log_payloads:
        # Google Cloud Logging uses 'trace' for correlation
        gcp_project = os.environ.get("GCP_PROJECT_ID", client.project)
        trace_id = f"projects/{gcp_project}/traces/{correlation_id}"

        logger.log_struct(
            payload, severity=payload.get("severity", "INFO"), trace=trace_id
        )


if __name__ == "__main__":
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
    else:
        request_id = str(uuid.uuid4())
        logs_to_write: list[StructuredLog] = [
            {
                "message": "Processing started for request.",
                "user_id": "user-54321",
                "severity": "INFO",
                "request_id": request_id,
                "context": {"service": "service-A"},
            },
            {
                "message": "Calling downstream service.",
                "user_id": "user-54321",
                "severity": "DEBUG",
                "request_id": request_id,
                "context": {"service": "service-B", "target": "service-C"},
            },
            {
                "message": "Processing finished for request.",
                "user_id": "user-54321",
                "severity": "INFO",
                "request_id": request_id,
                "context": {"service": "service-A", "duration_ms": 123},
            },
        ]
        write_correlated_log_entries(request_id, logs_to_write)
        print(f"Successfully wrote correlated logs with trace ID: {request_id}")
