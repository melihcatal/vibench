import os
import uuid
import time
from observability_client import get_gcp_logging_client, get_logger
from observability_models import StructuredLog

def write_correlated_logs_for_request():
    """
    Writes a sequence of correlated log entries for a simulated application
    request to Google Cloud Logging.
    """
    try:
        gcp_client = get_gcp_logging_client()
        logger_name = os.environ.get("GCP_LOG_NAME", "my_app_logs")
        logger = get_logger(gcp_client, name=logger_name)
        
        # A shared identifier for all logs related to this specific request
        correlation_id = str(uuid.uuid4())
        
        # Log 1: Request received
        log1 = StructuredLog(
            message="API request received: GET /items/item-789",
            severity="INFO",
            request_id=correlation_id,
            user_id="user-67890",
            http_request={"requestMethod": "GET", "requestUrl": "/items/item-789"}
        )
        logger.log_struct(log1.model_dump(mode='json'), severity=log1.severity)
        print(f"Logged request start for request_id: {correlation_id}")
        time.sleep(0.1) # Simulate work

        # Log 2: Backend operation
        log2 = StructuredLog(
            message="Fetching item from database.",
            severity="DEBUG",
            request_id=correlation_id,
            custom_dimensions={"db_query": "SELECT * FROM items WHERE id='item-789'"}
        )
        logger.log_struct(log2.model_dump(mode='json'), severity=log2.severity)
        print("Logged database fetch.")
        time.sleep(0.2) # Simulate work

        # Log 3: Request completed
        log3 = StructuredLog(
            message="API request completed successfully.",
            severity="INFO",
            request_id=correlation_id,
            http_request={"status": 200, "responseSize": "1024"}
        )
        logger.log_struct(log3.model_dump(mode='json'), severity=log3.severity)
        print("Logged request completion.")

    except Exception as e:
        print(f"An error occurred while writing correlated logs: {e}")

if __name__ == '__main__':
    write_correlated_logs_for_request()
