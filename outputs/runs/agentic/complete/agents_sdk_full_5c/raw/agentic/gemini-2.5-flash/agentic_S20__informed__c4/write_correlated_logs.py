import os
from google.cloud import logging

def write_correlated_logs(log_name: str, correlation_id: str, messages: list[dict]):
    """Writes application log events that include a shared request or correlation identifier.

    Each message dict should contain at least a 'message' key and optionally 'severity'.
    """
    client = logging.Client()
    logger = client.logger(log_name)

    entries = []
    for msg_data in messages:
        text_payload = msg_data.get("message", "")
        severity = msg_data.get("severity", "INFO")

        # Add a common label for correlation, or use trace/span if integrated with tracing
        log_entry = logging.LogEntry(
            json_payload={
                "message": text_payload,
                "correlation_id": correlation_id,
                **{k: v for k, v in msg_data.items() if k not in ['message', 'severity']}
            },
            severity=severity,
            # If integrated with a tracing system, you could set trace and span_id here
            # trace=f"projects/{client.project}/traces/{correlation_id}",
            # span_id="<SPAN_ID>",
        )
        entries.append(log_entry)

    logger.write(entries)
    print(f"Written {len(entries)} correlated log entries to {log_name} with correlation_id: {correlation_id}")

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_APPLICATION_CREDENTIALS environment variable or configure default credentials
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    log_name = f"projects/{project_id}/logs/my-app-request-logs"
    request_id = "req-abc-123"

    log_messages = [
        {"message": "Request received", "severity": "INFO", "endpoint": "/api/data"},
        {"message": "Processing data", "severity": "DEBUG", "step": "validate_input"},
        {"message": "Database query failed", "severity": "ERROR", "db_error_code": "1001"},
        {"message": "Request completed", "severity": "INFO"}
    ]

    write_correlated_logs(
        log_name=log_name,
        correlation_id=request_id,
        messages=log_messages
    )
