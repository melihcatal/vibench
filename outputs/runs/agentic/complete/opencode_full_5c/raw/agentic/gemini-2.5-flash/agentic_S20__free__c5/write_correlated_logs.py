from observability_client import get_logging_client
from observability_models import CorrelatedLogEntry
import os
import uuid


def write_correlated_logs(
    entries: list[CorrelatedLogEntry],
    log_name: str = "my-request-logs",
    trace_id: str = None,
):
    """Writes multiple log entries with a shared correlation ID to Google Cloud Logging.

    Args:
        entries: A list of CorrelatedLogEntry objects.
        log_name: The name of the log to write to.
        trace_id: An optional OpenTelemetry/Cloud Trace trace ID for stronger correlation.
                  If not provided, correlation_id from entries will be used as a label.
    """
    client = get_logging_client()
    logger = client.logger(log_name)

    batches = []
    for entry in entries:
        payload = (
            entry.json_payload if entry.json_payload else {"message": entry.message}
        )
        if entry.message and not entry.json_payload:
            payload["message"] = entry.message

        # Use trace_id if provided for stronger Google Cloud Trace integration
        # Otherwise, rely on custom 'correlation_id' label.
        entry_labels = {"correlation_id": entry.correlation_id, **entry.service_context}

        log_entry_data = {
            "jsonPayload": payload,
            "severity": entry.severity,
            "timestamp": entry.timestamp.isoformat() + "Z",
            "labels": entry_labels,
            "logName": f"projects/{client.project}/logs/{log_name}",
        }

        if trace_id:
            log_entry_data["trace"] = trace_id

        batches.append(log_entry_data)

    client.api.write_log_entries(batches)
    print(
        f"Correlated logs written to Google Cloud Logging with correlation_id/trace: {entries[0].correlation_id if not trace_id else trace_id}"
    )


if __name__ == "__main__":
    # Example Usage
    request_id = str(uuid.uuid4())

    # Example with custom correlation_id label
    log1 = CorrelatedLogEntry(
        correlation_id=request_id,
        message="Request started for user A",
        severity="INFO",
        json_payload={"user": "user-A", "path": "/api/data"},
    )
    log2 = CorrelatedLogEntry(
        correlation_id=request_id,
        message="Processing data for user A",
        severity="INFO",
        service_context={"service_name": "data-processor"},
    )
    log3 = CorrelatedLogEntry(
        correlation_id=request_id,
        message="Request completed for user A",
        severity="INFO",
        json_payload={"status": "success"},
    )
    write_correlated_logs([log1, log2, log3])

    # Example with Cloud Trace trace ID
    # In a real application, this trace_id would come from a trace context propagation header
    # For demonstration, generate a dummy one.
    dummy_trace_id = f"projects/{os.getenv('GCP_PROJECT_ID', 'your-gcp-project-id')}/traces/{uuid.uuid4().hex}"
    log4 = CorrelatedLogEntry(
        correlation_id=str(uuid.uuid4()),  # Still good to have this as a label
        message="Another request started",
        severity="INFO",
        json_payload={"user": "user-B", "method": "POST"},
    )
    log5 = CorrelatedLogEntry(
        correlation_id=str(uuid.uuid4()),
        message="Another request completed",
        severity="INFO",
        json_payload={"status": "201 Created"},
    )
    write_correlated_logs([log4, log5], trace_id=dummy_trace_id)
