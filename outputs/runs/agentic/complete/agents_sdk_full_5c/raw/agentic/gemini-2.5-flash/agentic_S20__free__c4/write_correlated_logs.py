from google.cloud import logging
import os
import uuid

def write_correlated_logs(log_name: str, correlation_id: str, messages: list[str], resource_type: str = "global", resource_labels: dict = None):
    """
    Writes application log events that include a shared request or correlation identifier.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = logging.Client(project=project_id)
    logger = client.logger(log_name)

    # The 'trace' field can be used for correlation.
    # Format: projects/PROJECT_ID/traces/TRACE_ID
    trace_path = f"projects/{project_id}/traces/{correlation_id}"

    for i, msg in enumerate(messages):
        entry = logging.LogEntry(
            text_payload=msg,
            severity="INFO",
            trace=trace_path,
            resource=logging.Resource(type=resource_type, labels=resource_labels or {})
        )
        logger.write(entry)
        print(f"Logged correlated event {i+1} to {log_name} with correlation_id {correlation_id}")

if __name__ == "__main__":
    # Example usage (requires GOOGLE_CLOUD_PROJECT env var and auth)
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    request_id = str(uuid.uuid4())
    log_messages = [
        f"Request {request_id}: User initiated action.",
        f"Request {request_id}: Processing data for user.",
        f"Request {request_id}: Action completed successfully."
    ]
    write_correlated_logs("my-app-requests", request_id, log_messages,
                          resource_type="cloud_run_revision",
                          resource_labels={
                              "service_name": "my-service",
                              "revision_name": "my-service-00001",
                              "location": "us-central1"
                          })
