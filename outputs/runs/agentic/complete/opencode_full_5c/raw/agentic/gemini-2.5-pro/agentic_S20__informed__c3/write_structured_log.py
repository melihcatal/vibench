import os
from observability_client import ObservabilityClient
from observability_models import LogEntry


def write_structured_log():
    """
    Writes a structured JSON log event to Google Cloud Logging.
    """
    client = ObservabilityClient()
    logger_name = os.getenv("GCP_LOG_NAME", "my-structured-log")

    log_entry = LogEntry(
        message="User signed in successfully.",
        severity="INFO",
        extra_data={
            "user_id": "user-12345",
            "ip_address": "192.168.1.100",
            "event_type": "user_login",
        },
    )

    client.write_log_entry(logger_name, log_entry)
    print(f"Successfully wrote structured log to {logger_name}.")


if __name__ == "__main__":
    write_structured_log()
