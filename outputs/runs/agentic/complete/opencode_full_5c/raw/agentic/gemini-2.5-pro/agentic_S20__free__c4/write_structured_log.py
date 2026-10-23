import os
import json
from datetime import datetime
from observability_client import get_logger
from observability_models import StructuredLog


def write_log_entry(log_data: StructuredLog):
    """Writes a structured log to Google Cloud Logging."""
    logger = get_logger("structured-log-writer")

    payload = log_data.model_dump(mode="json")

    # Google Cloud Logging uses 'severity' at the top level, not just in jsonPayload.
    severity = payload.pop("severity", "INFO")

    logger.log_struct(payload, severity=severity)
    print(
        f"Successfully wrote structured log with correlation ID: {log_data.correlation_id}"
    )


if __name__ == "__main__":
    # This is an example, it requires authentication with GCP
    # and the environment variable GCP_PROJECT_ID to be set.
    if os.environ.get("GCP_PROJECT_ID"):
        example_log = StructuredLog(
            message="User logged in successfully.",
            severity="INFO",
            correlation_id="a1b2c3d4-e5f6-7890-1234-567890abcdef",
            user_id="user-12345",
            request_method="POST",
            request_url="/auth/login",
            response_status=200,
            extra_data={"platform": "web", "region": "us-east-1"},
        )
        write_log_entry(example_log)
    else:
        print("GCP_PROJECT_ID environment variable not set. Skipping example run.")
