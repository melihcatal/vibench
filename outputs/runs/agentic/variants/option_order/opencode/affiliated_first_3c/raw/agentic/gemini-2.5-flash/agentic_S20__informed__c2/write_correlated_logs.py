import os
import uuid
from observability_client import get_logger


def write_correlated_log(
    log_name: str, correlation_id: str, message: str, severity: str = "INFO"
):
    """Writes a log entry with a correlation ID to Google Cloud Logging."""
    logger = get_logger(log_name)
    logger.log_text(
        text=message,
        severity=severity,
        labels={"correlation_id": correlation_id},
        # For Google Cloud Logging, trace can be used for correlation
        # trace=f"projects/{os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")}/traces/{correlation_id}",
    )
    print(f"Written correlated log to {log_name} with ID {correlation_id}: {message}")


if __name__ == "__main__":
    LOG_NAME = "my-correlated-app-log"
    correlation_id_1 = str(uuid.uuid4())
    correlation_id_2 = str(uuid.uuid4())

    write_correlated_log(
        LOG_NAME, correlation_id_1, "Starting process for request X.", "INFO"
    )
    write_correlated_log(
        LOG_NAME, correlation_id_1, "Step 1 completed for request X.", "INFO"
    )
    write_correlated_log(LOG_NAME, correlation_id_2, "Processing image Y.", "DEBUG")
    write_correlated_log(
        LOG_NAME,
        correlation_id_1,
        "Error in sub-process for request X: Failed to acquire lock.",
        "ERROR",
    )
    write_correlated_log(
        LOG_NAME, correlation_id_2, "Image Y processed successfully.", "INFO"
    )
