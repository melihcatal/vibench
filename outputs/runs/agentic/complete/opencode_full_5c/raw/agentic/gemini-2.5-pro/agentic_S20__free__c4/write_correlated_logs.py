import os
import uuid
from observability_client import get_logger
from observability_models import StructuredLog


def write_application_logs():
    """
    Writes a series of application log events with a shared
    correlation identifier to Google Cloud Logging.
    """
    logger = get_logger("correlated-log-writer")
    correlation_id = str(uuid.uuid4())

    log_entries = [
        StructuredLog(
            message="Processing new user registration request.",
            severity="INFO",
            correlation_id=correlation_id,
            user_id="new-user-abc",
            request_method="POST",
            request_url="/users/register",
        ),
        StructuredLog(
            message="Validated user input successfully.",
            severity="DEBUG",
            correlation_id=correlation_id,
            user_id="new-user-abc",
            extra_data={"validation_rules": ["not_empty", "is_email"]},
        ),
        StructuredLog(
            message="Database transaction started for user creation.",
            severity="DEBUG",
            correlation_id=correlation_id,
            user_id="new-user-abc",
        ),
        StructuredLog(
            message="User created successfully in database.",
            severity="INFO",
            correlation_id=correlation_id,
            user_id="new-user-abc",
            response_status=201,
        ),
    ]

    for entry in log_entries:
        payload = entry.model_dump(mode="json")
        severity = payload.pop("severity", "INFO")
        logger.log_struct(payload, severity=severity)
        print(f"Logged event: '{entry.message}' with correlation ID: {correlation_id}")


if __name__ == "__main__":
    if os.environ.get("GCP_PROJECT_ID"):
        write_application_logs()
    else:
        print("GCP_PROJECT_ID environment variable not set. Skipping example run.")
