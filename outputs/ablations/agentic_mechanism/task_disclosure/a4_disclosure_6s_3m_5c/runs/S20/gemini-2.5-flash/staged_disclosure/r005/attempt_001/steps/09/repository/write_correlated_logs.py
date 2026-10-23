import google.cloud.logging
import os
import uuid

def write_correlated_logs(project_id: str, log_name: str, correlation_id: str):
    """
    Writes application log events with a shared request or correlation identifier to Google Cloud Logging.

    Args:
        project_id: The Google Cloud project ID.
        log_name: The name of the log to write to (e.g., "my-application-logs").
        correlation_id: A unique identifier for a series of related log entries.
    """
    client = google.cloud.logging.Client(project=project_id)
    logger = client.logger(log_name)

    # Example log entries with the same correlation_id
    logger.log_struct(
        {
            "message": "Starting request processing.",
            "correlation_id": correlation_id,
            "severity": "INFO",
            "component": "api_gateway",
        },
        severity="INFO"
    )
    logger.log_struct(
        {
            "message": "Processing user data.",
            "correlation_id": correlation_id,
            "severity": "INFO",
            "user_id": "user-123",
            "component": "user_service",
        },
        severity="INFO"
    )
    logger.log_struct(
        {
            "message": "Request completed successfully.",
            "correlation_id": correlation_id,
            "severity": "INFO",
            "response_time_ms": 150,
            "component": "api_gateway",
        },
        severity="INFO"
    )

if __name__ == "__main__":
    # Replace with your Google Cloud Project ID
    # You might also set GOOGLE_CLOUD_PROJECT environment variable
    # For local testing, ensure your GOOGLE_APPLICATION_CREDENTIALS are set up
    # or you have authenticated via `gcloud auth application-default login`
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    if project_id == "your-gcp-project-id":
        print("WARNING: Please set the GOOGLE_CLOUD_PROJECT environment variable or replace 'your-gcp-project-id' with your actual GCP Project ID.")
        print("Logs will attempt to be written, but may fail if authentication/project ID is not configured.")

    log_name = "my-application-logs"
    new_correlation_id = str(uuid.uuid4())
    print(f"Writing logs for correlation ID: {new_correlation_id}")
    write_correlated_logs(project_id, log_name, new_correlation_id)
    print("Log events sent to Google Cloud Logging.")
    print("You can view these logs in the Google Cloud Console under Logging > Log Explorer.")
