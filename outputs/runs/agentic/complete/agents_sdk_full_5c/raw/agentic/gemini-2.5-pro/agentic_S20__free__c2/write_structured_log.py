import datetime
import os
from observability_client import logging_client
from observability_models import StructuredLog

def write_json_log(log_entry: StructuredLog, logger_name: str = "structured_log_writer"):
    """
    Writes a structured JSON log to Google Cloud Logging.

    Args:
        log_entry: A StructuredLog object containing the log data.
        logger_name: The name of the logger to use.
    """
    if not logging_client:
        print("Logging client not available. Skipping log write.")
        return

    # The google-cloud-logging library automatically handles
    # converting a dictionary to the jsonPayload field.
    payload = {
        "message": log_entry.message,
        "user": {"id": log_entry.user_id},
        "httpRequest": {
            "requestMethod": log_entry.http_method,
            "requestUrl": log_entry.resource,
            "status": log_entry.http_status,
            "latency": f"{log_entry.latency_ms / 1000}s",
            "requestId": log_entry.request_id,
        },
        "custom_data": log_entry.additional_data,
    }

    logger = logging_client.get_logger(logger_name)
    logger.log_struct(payload, severity="INFO")

    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    print(f"Successfully wrote structured log to Google Cloud Logging for project '{project_id}'.")

if __name__ == "__main__":
    # Example structured log
    example_log = StructuredLog(
        message="User authenticated successfully.",
        user_id="user-9876",
        request_id="a7b1c2d3-e4f5-4a6b-8c7d-9e8f7a6b5c4d",
        http_method="POST",
        resource="/api/v1/login",
        http_status=200,
        latency_ms=150,
        additional_data={"login_type": "password"}
    )
    try:
        write_json_log(example_log)
    except Exception as e:
        print(f"An error occurred: {e}")
