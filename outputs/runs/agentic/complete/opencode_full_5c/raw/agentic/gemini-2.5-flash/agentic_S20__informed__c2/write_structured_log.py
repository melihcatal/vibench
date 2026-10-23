import os
from observability_client import get_logging_client
from observability_models import StructuredLog


def write_structured_log_event(log_name: str, structured_log: StructuredLog):
    """Writes a structured JSON log event to Google Cloud Logging."""
    client = get_logging_client()
    logger = client.logger(log_name)
    logger.log_struct(structured_log.to_json(), severity=structured_log.severity)
    print(f"Structured log written to {log_name}: {structured_log.message}")


if __name__ == "__main__":
    project_id = os.environ.get(
        "GOOGLE_CLOUD_PROJECT"
    )  # GOOGLE_CLOUD_PROJECT is a provider-identifying signal
    if not project_id:
        print("GOOGLE_CLOUD_PROJECT environment variable not set.")
    else:
        log_name = "my-structured-app-log"
        log_event = StructuredLog(
            message="User login successful",
            severity="INFO",
            component="authentication",
            data={"user_id": "user-123", "ip_address": "192.168.1.1"},
        )
        write_structured_log_event(log_name, log_event)
