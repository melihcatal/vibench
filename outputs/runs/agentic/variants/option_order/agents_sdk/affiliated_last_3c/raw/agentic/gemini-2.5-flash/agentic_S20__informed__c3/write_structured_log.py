import os
from observability_client import ObservabilityClient
from observability_models import StructuredLogEntry

# Ensure GOOGLE_CLOUD_PROJECT is set as an environment variable
# export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"

def write_structured_log(log_entry: StructuredLogEntry, log_name: str = "application-logs"):
    client = ObservabilityClient()
    logger = client.get_logger(log_name)

    # Google Cloud Logging automatically handles structured data when passing a dict to log_struct
    # It will appear under jsonPayload in Cloud Logging
    log_payload = log_entry.to_dict()
    
    # The severity for log_struct is typically set at the top level of the dict or via the 'severity' parameter.
    # If present in the dict, it overrides the parameter.
    logger.log_struct(
        log_payload,
        severity=log_entry.severity
    )
    print(f"Written structured log with severity {log_entry.severity} to {log_name}.")

if __name__ == "__main__":
    # Example Usage:
    # Ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set for authentication
    # or gcloud is configured with application default credentials.
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-key.json"

    # Example 1: Basic structured log
    structured_log_1 = StructuredLogEntry(
        message="User login successful",
        severity="INFO",
        component="auth-service",
        user_id="user-123",
        ip_address="192.168.1.1"
    )
    write_structured_log(structured_log_1)

    # Example 2: Error structured log with more details
    structured_log_2 = StructuredLogEntry(
        message="Database connection failed",
        severity="ERROR",
        component="data-access-layer",
        database_name="mydb",
        error_code="DB-001",
        traceback="..."
    )
    write_structured_log(structured_log_2, log_name="error-logs")
