import os
import uuid
from observability_client import get_logging_client
from observability_models import create_structured_log_entry

PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT")  # Ensure this env var is set
LOG_NAME = "my-application-log"


def write_correlated_logs(request_id: str):
    client = get_logging_client()
    logger = client.logger(LOG_NAME)

    # Log entry 1
    entry1 = create_structured_log_entry(
        message="Starting request processing",
        severity="INFO",
        component="api-gateway",
        correlation_id=request_id,
        data={"endpoint": "/api/v1/data", "method": "GET"},
    )
    logger.log_struct(entry1)
    print(f"Correlated log 1 written for request {request_id}")

    # Log entry 2
    entry2 = create_structured_log_entry(
        message="Fetching data from backend",
        severity="DEBUG",
        component="data-service",
        correlation_id=request_id,
        data={"database": "mydb", "query": "SELECT * FROM users"},
    )
    logger.log_struct(entry2)
    print(f"Correlated log 2 written for request {request_id}")

    # Log entry 3
    entry3 = create_structured_log_entry(
        message="Finished request processing",
        severity="INFO",
        component="api-gateway",
        correlation_id=request_id,
        data={"status": "success", "response_time_ms": 150},
    )
    logger.log_struct(entry3)
    print(f"Correlated log 3 written for request {request_id}")


if __name__ == "__main__":
    new_request_id = str(uuid.uuid4())
    write_correlated_logs(new_request_id)
