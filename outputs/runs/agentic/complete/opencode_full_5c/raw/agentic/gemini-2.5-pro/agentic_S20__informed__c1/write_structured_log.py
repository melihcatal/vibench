import os
import json
from observability_client import get_logging_client
from observability_models import LogEntry


def write_log(log_entry: LogEntry, log_name: str = "my-structured-log"):
    """Writes a structured JSON log to Google Cloud Logging.

    Args:
        log_entry: A dictionary representing the structured log.
        log_name: The name of the log to write to.
    """
    logging_client = get_logging_client()
    logger = logging_client.logger(log_name)

    logger.log_json(log_entry)

    print(f"Wrote structured log to {log_name}: {json.dumps(log_entry)}")


if __name__ == "__main__":
    # Example Usage:
    # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable before running.
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account-file.json"

    # The project ID is inferred from the environment if not set explicitly.
    # project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    # if not project_id:
    #     raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    sample_log = {
        "message": "User signed in successfully.",
        "user_id": "user_12345",
        "ip_address": "192.168.1.100",
        "activity_type": "authentication",
    }
    write_log(sample_log)
