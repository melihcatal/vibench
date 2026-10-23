from observability_client import ObservabilityClient
from observability_models import LogEntry
import uuid


def write_correlated_logs(log_entries: list[LogEntry]):
    client = ObservabilityClient()
    logger = client.get_logger()

    # Generate a single trace ID for all correlated logs in this batch
    correlation_id = str(uuid.uuid4())

    for log_entry in log_entries:
        # Google Cloud Logging uses 'trace' field for correlation
        # The format for trace is projects/PROJECT_ID/traces/TRACE_ID
        # We'll use a simplified correlation_id here and demonstrate adding it to labels or json_payload
        # For actual tracing, integrate with OpenTelemetry or Google Cloud Trace

        log_entry.labels["correlation_id"] = correlation_id
        if log_entry.json_payload:
            log_entry.json_payload["correlation_id"] = correlation_id
        else:
            log_entry.json_payload = {
                "correlation_id": correlation_id,
                "message": log_entry.message,
            }

        logger.log_struct(
            log_entry.json_payload,
            severity=log_entry.severity,
            labels=log_entry.labels,
        )
        print(
            f"Correlated log written (correlation_id: {correlation_id}, severity: {log_entry.severity})"
        )


if __name__ == "__main__":
    # Example usage
    entries = [
        LogEntry(message="Request received for /api/data", severity="INFO"),
        LogEntry(message="Processing data item X", severity="DEBUG"),
        LogEntry(message="Response sent for /api/data", severity="INFO"),
    ]
    write_correlated_logs(entries)
