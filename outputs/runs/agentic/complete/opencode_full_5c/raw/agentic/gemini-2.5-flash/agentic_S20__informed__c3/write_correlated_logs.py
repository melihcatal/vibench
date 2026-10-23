from observability_client import get_logging_client
from observability_models import format_log_entry
import os
import uuid


def write_correlated_logs(log_name, request_id, user_id=None):
    """Writes application log events that include a shared request or correlation identifier.

    Args:
        log_name (str): The name of the log to write to.
        request_id (str): A unique identifier for the request/correlation.
        user_id (str, optional): An optional user identifier.
    """
    client = get_logging_client()
    logger = client.logger(log_name)

    common_fields = {"request_id": request_id}
    if user_id:  # Only add user_id if it's not None
        common_fields["user_id"] = user_id

    # Simulate multiple log events for the same request
    log_entry_1 = format_log_entry(
        "Starting request processing", severity="INFO", step="start", **common_fields
    )
    logger.log_struct(log_entry_1["jsonPayload"], severity=log_entry_1["severity"])

    log_entry_2 = format_log_entry(
        "Fetching data from external service",
        severity="INFO",
        step="fetch_data",
        service="external-api",
        **common_fields,
    )
    logger.log_struct(log_entry_2["jsonPayload"], severity=log_entry_2["severity"])

    log_entry_3 = format_log_entry(
        "Data processing complete",
        severity="INFO",
        step="complete",
        duration_ms=150,
        **common_fields,
    )
    logger.log_struct(log_entry_3["jsonPayload"], severity=log_entry_3["severity"])

    print(
        f"Correlated logs with request_id '{request_id}' written to Google Cloud Logging: {log_name}"
    )


if __name__ == "__main__":
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        # Generate a unique request ID for demonstration
        correlation_id = str(uuid.uuid4())
        write_correlated_logs(
            log_name="my-correlated-app-logs",
            request_id=correlation_id,
            user_id="demo-user-456",
        )
