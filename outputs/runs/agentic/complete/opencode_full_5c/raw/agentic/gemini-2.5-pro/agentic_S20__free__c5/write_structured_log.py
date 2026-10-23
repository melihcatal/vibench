import os
import json
from observability_client import get_log_writer_client
from observability_models import StructuredLog


def write_log_entry(log_name: str, log_payload: StructuredLog):
    """Writes a structured log entry to Google Cloud Logging.

    Args:
        log_name: The name of the log to write to.
        log_payload: A StructuredLog object representing the log entry.
    """
    client = get_log_writer_client()
    logger = client.logger(log_name)

    payload = log_payload.model_dump_json(exclude_none=True)

    # In a real application, you might add more resource information
    # For example:
    # resource = Resource(type="gce_instance", labels={"instance_id": "your-instance-id", "zone": "your-zone"})
    # logger.log_struct(json.loads(payload), severity=log_payload.severity, resource=resource)

    logger.log_struct(json.loads(payload), severity=log_payload.severity)

    print(f"Wrote structured log to {log_name}")


if __name__ == "__main__":
    # Example Usage:
    # Set the GOOGLE_CLOUD_PROJECT environment variable
    if not os.environ.get("GOOGLE_CLOUD_PROJECT"):
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
    else:
        log_entry = StructuredLog(
            message="User signed up successfully.",
            severity="INFO",
            context={"user_id": "user-12345", "event_type": "signup"},
        )
        write_log_entry("my-structured-log", log_entry)
