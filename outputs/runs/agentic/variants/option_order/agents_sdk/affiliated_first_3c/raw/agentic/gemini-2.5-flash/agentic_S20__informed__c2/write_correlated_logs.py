from google.cloud import logging
import uuid
import os

def write_correlated_logs(log_name: str, correlation_id: str, messages: list[dict]):
    """Writes application log events that include a shared request or correlation identifier to Google Cloud Logging.
    Each message dict should contain 'message', 'severity', and any other desired fields.
    """
    client = logging.Client()
    logger = client.logger(log_name)

    entries = []
    for msg_data in messages:
        # Google Cloud Logging uses 'trace' for correlation, often in the format projects/PROJECT_ID/traces/TRACE_ID
        # For simplicity, we'll use a custom field and also try to map to trace if possible.
        # If you have a real OpenTelemetry or Cloud Trace setup, you'd integrate with that.
        
        # Add correlation_id to the log entry payload as a custom field
        # For Cloud Trace integration, typically `trace` and `span_id` would be set.
        # Here we'll just add it as a custom field and also use it in trace if it's a UUID.
        
        payload = {
            "correlation_id": correlation_id,
            "message": msg_data.get("message", ""),
            **{k: v for k, v in msg_data.items() if k not in ["message", "severity"]}
        }

        entry = logging.LogEntry(
            json_payload=payload,
            severity=msg_data.get("severity", "INFO"),
            # If correlation_id is a valid trace ID, you could set trace directly.
            # For a more robust solution, integrate with OpenTelemetry or Google Cloud Trace client.
            # Example trace format: projects/PROJECT_ID/traces/TRACE_ID
        )
        entries.append(entry)
    
    # Batch write logs
    logger.write(entries)
    print(f"{len(entries)} correlated log entries written to Google Cloud Logging (log_name: {log_name}, correlation_id: {correlation_id})")

if __name__ == "__main__":
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("GOOGLE_CLOUD_PROJECT environment variable not set. Please set it to your GCP project ID.")
        exit(1)

    log_name = f"projects/{project_id}/logs/my-app-request-logs"
    
    request_correlation_id = str(uuid.uuid4())
    
    log_messages = [
        {"message": "Request started", "step": "init", "severity": "INFO"},
        {"message": "Processing data", "data_size_kb": 1024, "severity": "INFO"},
        {"message": "Database query failed", "error": "timeout", "severity": "ERROR"},
        {"message": "Request finished", "status": "failed", "severity": "INFO"},
    ]

    write_correlated_logs(
        log_name=log_name,
        correlation_id=request_correlation_id,
        messages=log_messages
    )

    another_correlation_id = str(uuid.uuid4())
    log_messages_2 = [
        {"message": "Another request started", "severity": "INFO"},
        {"message": "Another request completed successfully", "status": "success", "severity": "INFO"},
    ]
    write_correlated_logs(
        log_name=log_name,
        correlation_id=another_correlation_id,
        messages=log_messages_2
    )
