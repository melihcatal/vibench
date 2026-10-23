import os
from observability_client import get_logging_client
from observability_models import create_structured_log_entry

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")  # Ensure this env var is set
LOG_NAME = "my-application-log"


def write_structured_log(
    message: str, severity: str, component: str, data: dict = None
):
    client = get_logging_client()
    logger = client.logger(LOG_NAME)
    entry = create_structured_log_entry(message, severity, component, data)
    logger.log_struct(entry)
    print(f"Structured log written: {message}")


if __name__ == "__main__":
    write_structured_log(
        message="User login attempt",
        severity="INFO",
        component="authentication",
        data={"user_id": "user-123", "ip_address": "192.168.1.10"},
    )
