import datetime
from typing import Dict, Any, Optional
from observability_client import ObservabilityClient


def write_correlated_log(
    log_name: str,
    severity: str,
    message: str,
    correlation_id: str,
    span_id: Optional[str] = None,
    trace_id: Optional[str] = None,
    json_payload: Dict[str, Any] = None,
    resource_type: str = "global",
    resource_labels: Dict[str, str] = None,
    labels: Dict[str, str] = None,
):
    """Writes an application log event with a shared request/correlation identifier to Google Cloud Logging.

    Args:
        log_name: The name of the log to write to.
        severity: The severity of the log entry (e.g., "INFO", "ERROR").
        message: The main message of the log entry.
        correlation_id: A shared identifier to correlate log entries.
        span_id: The OpenTelemetry Span ID.
        trace_id: The OpenTelemetry Trace ID.
        json_payload: Optional structured JSON payload.
        resource_type: The type of resource (e.g., "global", "gce_instance").
        resource_labels: Labels for the resource.
        labels: Additional labels for the log entry.
    """
    client = ObservabilityClient().logging_client

    # Construct the LogEntry object
    entry_json = {
        "severity": severity.upper(),
        "textPayload": message,
        "resource": {
            "type": resource_type,
            "labels": resource_labels
            if resource_labels is not None
            else {"project_id": client.project},
        },
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "labels": labels if labels is not None else {},
    }

    # Add correlation_id to labels for easier filtering/grouping
    entry_json["labels"]["correlation_id"] = correlation_id

    # Add OpenTelemetry trace/span info if available
    if trace_id:
        # Google Cloud Logging expects trace format projects/<PROJECT_ID>/traces/<TRACE_ID>
        entry_json["trace"] = f"projects/{client.project}/traces/{trace_id}"
    if span_id:
        entry_json["spanId"] = span_id

    if json_payload:
        entry_json["jsonPayload"] = json_payload

    logger = client.logger(log_name)

    # Use log_struct if there is a jsonPayload, otherwise use log_text
    if "jsonPayload" in entry_json:
        logger.log_struct(
            entry_json["jsonPayload"],
            severity=entry_json["severity"],
            text_payload=entry_json["textPayload"],
            resource=entry_json["resource"],
            labels=entry_json["labels"],
            trace=entry_json.get("trace"),
            span_id=entry_json.get("spanId"),
        )
    else:
        logger.log_text(
            entry_json["textPayload"],
            severity=entry_json["severity"],
            resource=entry_json["resource"],
            labels=entry_json["labels"],
            trace=entry_json.get("trace"),
            span_id=entry_json.get("spanId"),
        )

    print(
        f"Wrote correlated log to {log_name} with severity {severity} and correlation_id {correlation_id}."
    )


if __name__ == "__main__":
    # Example usage
    LOG_NAME = "my-correlated-app-log"
    CORRELATION_ID = "req-abc-123"
    TRACE_ID = "c23b3f2a5d2a4e2b8c9d0e1f2a3b4c5d"
    SPAN_ID = "a1b2c3d4e5f6a7b8"

    # First log entry for a request
    write_correlated_log(
        LOG_NAME,
        "INFO",
        "Starting request processing",
        CORRELATION_ID,
        trace_id=TRACE_ID,
        span_id=SPAN_ID,
        json_payload={"endpoint": "/api/v1/data", "method": "GET"},
    )

    # Second log entry, correlated to the first
    write_correlated_log(
        LOG_NAME,
        "DEBUG",
        "Fetching data from database",
        CORRELATION_ID,
        trace_id=TRACE_ID,
        span_id=SPAN_ID,
        json_payload={"query": "SELECT * FROM data"},
    )

    # An error log, also correlated
    write_correlated_log(
        LOG_NAME,
        "ERROR",
        "Database query failed",
        CORRELATION_ID,
        trace_id=TRACE_ID,
        json_payload={"error_code": 500, "details": "Connection refused"},
    )
