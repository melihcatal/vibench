import os
import datetime
from observability_client import get_gcp_logging_client, get_logger
from observability_models import StructuredLog

def write_single_structured_log():
    """
    Writes a single structured log entry to Google Cloud Logging.
    """
    try:
        # Initialize the Google Cloud Logging client
        gcp_client = get_gcp_logging_client()
        logger_name = os.environ.get("GCP_LOG_NAME", "my_app_logs")
        logger = get_logger(gcp_client, name=logger_name)

        # Create a structured log record
        log_entry = StructuredLog(
            message="User logged in successfully.",
            severity="INFO",
            user_id="user-12345",
            http_request={
                "requestMethod": "POST",
                "requestUrl": "/auth/login",
                "status": 200,
                "userAgent": "MyClient/1.0.0"
            },
            custom_dimensions={"login_type": "password"}
        )

        # Write the log
        # The `json_payload` field is used by Google Cloud Logging for structured logs
        logger.log_struct(log_entry.model_dump(mode='json'), severity=log_entry.severity)

        print(f"Successfully wrote structured log for trace: {log_entry.trace_id}")

    except Exception as e:
        print(f"An error occurred while writing a structured log: {e}")

if __name__ == '__main__':
    # For this to work, ensure GOOGLE_APPLICATION_CREDENTIALS and GOOGLE_CLOUD_PROJECT
    # are set in your environment.
    write_single_structured_log()
