
import os
import datetime
from observability_client import get_gcp_logging_client
from observability_models import StructuredLog

def write_log_entry(log_name: str, log_payload: dict):
    """
    Writes a structured log entry to Google Cloud Logging.

    :param log_name: The name of the log to write to.
    :param log_payload: A dictionary representing the structured log.
    """
    logging_client = get_gcp_logging_client()
    logger = logging_client.logger(log_name)
    
    logger.log_json(log_payload)
    
    print(f"Successfully wrote log to {log_name}")


if __name__ == '__main__':
    log_data = StructuredLog(
        message="User signed up successfully.",
        severity="INFO",
        user_id="user_12345",
        service_context="user-service",
        custom_dimensions={
            "plan_type": "free",
            "signup_method": "google-oauth"
        },
        http_request={
            "requestMethod": "POST",
            "requestUrl": "/api/users",
            "status": 201,
            "userAgent": "MyClient/1.0.0",
            "remoteIp": "192.0.2.1"
        }
    )
    
    # In a real app, LOG_NAME might come from config
    LOG_NAME = os.getenv("GCP_LOG_NAME", "my-structured-log")
    write_log_entry(LOG_NAME, log_data.to_dict())
