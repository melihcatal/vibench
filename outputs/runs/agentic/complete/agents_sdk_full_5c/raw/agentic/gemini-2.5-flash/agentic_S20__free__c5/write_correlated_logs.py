from observability_client import get_logging_client
from observability_models import create_log_entry
import os
import uuid

PROJECT_ID = os.environ.get("GCP_PROJECT_ID", "your-gcp-project-id")
LOG_NAME = "my-correlated-app-logs"

def write_correlated_logs(correlation_id: str, events: list[dict]):
    """Writes application log events that include a shared request or correlation identifier.

    Args:
        correlation_id: A unique identifier to link related log entries.
        events: A list of dictionaries, where each dict represents a log event
                (e.g., {'message': '...', 'severity': '...', 'data': {...}}).
    """
    client = get_logging_client()
    logger = client.logger(LOG_NAME)

    for event in events:
        message = event.get('message', 'No message provided')
        severity = event.get('severity', 'INFO')
        event_data = event.get('data', {})
        
        # Add correlation_id to the structured log payload
        log_payload = create_log_entry(
            message=message,
            severity=severity,
            correlationId=correlation_id, # Use camelCase for consistency with GCP
            **event_data
        )

        logger.log_struct(log_payload, severity=severity)
        print(f"Wrote correlated log to Google Cloud Logging (ID: {correlation_id}): {log_payload}")

if __name__ == '__main__':
    # Example usage
    request_id = str(uuid.uuid4())
    log_events = [
        {
            "message": "Request received",
            "severity": "INFO",
            "data": {"path": "/api/v1/data", "method": "GET"}
        },
        {
            "message": "Processing data",
            "severity": "DEBUG",
            "data": {"record_count": 100}
        },
        {
            "message": "Response sent",
            "severity": "INFO",
            "data": {"status_code": 200, "duration_ms": 50}
        },
    ]
    write_correlated_logs(request_id, log_events)
