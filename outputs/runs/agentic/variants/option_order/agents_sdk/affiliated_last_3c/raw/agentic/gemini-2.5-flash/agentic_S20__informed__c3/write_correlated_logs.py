import os
from observability_client import ObservabilityClient
from observability_models import CorrelatedLogEntry
import uuid

# Ensure GOOGLE_CLOUD_PROJECT is set as an environment variable
# export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"

def write_correlated_logs(log_entries: list[CorrelatedLogEntry], log_name: str = "application-logs"):
    client = ObservabilityClient()
    logger = client.get_logger(log_name)

    for entry in log_entries:
        # Google Cloud Logging automatically handles structured data when passing a dict to log_struct
        # The 'correlationId' will appear as a field in jsonPayload
        log_payload = entry.to_dict()
        logger.log_struct(
            log_payload,
            severity=entry.severity
        )
        print(f"Written correlated log with correlation ID {entry.correlation_id} and severity {entry.severity} to {log_name}.")

if __name__ == "__main__":
    # Example Usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication
    # or gcloud is configured with application default credentials.
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"

    correlation_id = str(uuid.uuid4())
    print(f"Generated correlation ID: {correlation_id}")

    # Simulate a series of events for a single request
    correlated_logs = [
        CorrelatedLogEntry(
            message="Request received for /api/v1/resource",
            correlation_id=correlation_id,
            severity="INFO",
            method="GET",
            path="/api/v1/resource"
        ),
        CorrelatedLogEntry(
            message="Processing data for resource",
            correlation_id=correlation_id,
            severity="DEBUG",
            processor="data-processor-a"
        ),
        CorrelatedLogEntry(
            message="Successfully fetched resource data",
            correlation_id=correlation_id,
            severity="INFO",
            data_size_kb=120
        ),
        CorrelatedLogEntry(
            message="Response sent for /api/v1/resource",
            correlation_id=correlation_id,
            severity="INFO",
            status_code=200
        )
    ]
    write_correlated_logs(correlated_logs)

    # Example with an error in the correlation flow
    error_correlation_id = str(uuid.uuid4())
    print(f"Generated error correlation ID: {error_correlation_id}")
    error_logs = [
        CorrelatedLogEntry(
            message="Initiating file upload",
            correlation_id=error_correlation_id,
            severity="INFO",
            file_name="report.pdf"
        ),
        CorrelatedLogEntry(
            message="File upload failed due to network error",
            correlation_id=error_correlation_id,
            severity="ERROR",
            error_details="Connection reset by peer",
            retry_attempt=1
        )
    ]
    write_correlated_logs(error_logs, log_name="file-upload-logs")
