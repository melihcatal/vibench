import os
import json
from observability_client import get_logging_client


def write_log(logger_name: str, message: str, metadata: dict):
    """
    Writes a single structured log entry to Google Cloud Logging.

    Args:
        logger_name: The name of the logger to use.
        message: The primary log message.
        metadata: A dictionary of structured data to include.
    """
    client = get_logging_client()
    logger = client.logger(logger_name)

    log_payload = {
        "message": message,
        "service": "application-backend",
        "version": "1.0.0",
        **metadata,
    }

    logger.log_json(log_payload, severity="INFO")
    print(f"Successfully wrote structured log to '{logger_name}'.")


if __name__ == "__main__":
    if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS"):
        test_metadata = {
            "user_id": "user_12345",
            "transaction_id": "txn_67890",
            "http_request": {
                "requestMethod": "GET",
                "requestUrl": "/api/v1/products",
                "status": 200,
                "userAgent": "MyTestClient/1.0",
            },
        }
        write_log("structured_log_writer", "User requested product list", test_metadata)
    else:
        print("GOOGLE_APPLICATION_CREDENTIALS not set. Skipping example run.")
