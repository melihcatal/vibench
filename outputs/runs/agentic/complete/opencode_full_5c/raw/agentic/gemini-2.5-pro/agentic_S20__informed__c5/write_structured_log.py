import json
from observability_client import get_gcp_logger
from observability_models import StructuredLog


def write_structured_log(log_name: str, log_entry: StructuredLog):
    """
    Writes a structured JSON log to Google Cloud Logging.

    Args:
        log_name: The name of the log to write to.
        log_entry: A StructuredLog object containing the log data.
    """
    logger = get_gcp_logger(log_name)

    logger.log_struct(log_entry.to_dict(), severity=log_entry.severity)
    print(f"Wrote structured log to {log_name}")


if __name__ == "__main__":
    # Example Usage:
    # Set GOOGLE_APPLICATION_CREDENTIALS and GCP_PROJECT_ID environment variables
    # before running this script.

    request_log = StructuredLog(
        message="User signed in successfully.",
        user_id="user_12345",
        request_id="abc-123-xyz-789",
        severity="INFO",
    )

    write_structured_log("my-structured-log", request_log)
