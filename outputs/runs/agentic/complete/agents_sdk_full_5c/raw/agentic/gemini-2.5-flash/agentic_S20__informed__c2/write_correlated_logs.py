import datetime
import uuid
from observability_client import get_logging_client, get_project_id

def write_correlated_logs(log_name: str, correlation_id: str, messages: list):
    """Writes application log events with a shared request/correlation identifier to Google Cloud Logging."""
    client = get_logging_client()
    logger = client.logger(log_name)

    for i, message_text in enumerate(messages):
        payload = {
            "message": message_text,
            "correlation_id": correlation_id,
            "sequence": i + 1,
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z"
        }
        # Labels are good for indexing/filtering at a high level
        labels = {"correlation_id": correlation_id}

        logger.log_struct(payload, severity="INFO", labels=labels)
        print(f"Wrote log with correlation_id {correlation_id}: {message_text}")

if __name__ == "__main__":
    project_id = get_project_id()
    log_name = "my-app-request-logs"
    request_correlation_id = str(uuid.uuid4())

    application_events = [
        "Request received for processing",
        "Processing user input data",
        "Fetching data from external service",
        "External service responded successfully",
        "Generating final report",
        "Request completed successfully"
    ]

    write_correlated_logs(log_name, request_correlation_id, application_events)

    another_correlation_id = str(uuid.uuid4())
    another_events = [
        "Batch job started",
        "Processing item 1 of 100",
        "Item 1 processed with warning",
        "Batch job finished"
    ]
    write_correlated_logs(log_name, another_correlation_id, another_events)
