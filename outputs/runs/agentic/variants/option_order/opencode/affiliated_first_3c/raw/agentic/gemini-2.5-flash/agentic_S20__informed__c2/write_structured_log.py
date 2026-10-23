import os
from observability_client import get_logger
from observability_models import StructuredLog


def write_structured_log(log_name: str, log_entry: StructuredLog):
    """Writes a structured log entry to Google Cloud Logging."""
    logger = get_logger(log_name)
    logger.log_struct(
        info={
            "message": log_entry.message,
            "severity": log_entry.severity,
            "component": log_entry.component,
            "metadata": log_entry.metadata,
        },
        severity=log_entry.severity,
    )
    print(f"Written structured log to {log_name}: {log_entry.message}")


if __name__ == "__main__":
    PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
    LOG_NAME = "my-structured-app-log"
    example_log = StructuredLog(
        message="User login successful",
        severity="INFO",
        component="auth-service",
        metadata={"user_id": "user-123", "ip_address": "192.168.1.1"},
    )
    write_structured_log(LOG_NAME, example_log)
