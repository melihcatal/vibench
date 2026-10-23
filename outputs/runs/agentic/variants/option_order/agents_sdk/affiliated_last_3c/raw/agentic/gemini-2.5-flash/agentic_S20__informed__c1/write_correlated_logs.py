from google.cloud import logging
import os
import uuid

def write_correlated_logs(request_id: str, messages: list[str], component: str = "example-app"):
    client = logging.Client()
    logger = client.logger("application-logs")

    for message in messages:
        log_entry = {
            "message": message,
            "severity": "INFO",
            "component": component,
            "request_id": request_id,
            "environment": os.getenv("ENVIRONMENT", "development")
        }
        logger.log_struct(log_entry)

if __name__ == "__main__":
    correlation_id = str(uuid.uuid4())
    write_correlated_logs(
        correlation_id,
        [
            "Processing user request for data",
            "Fetching data from database",
            "Data retrieval complete"
        ],
        "data-service"
    )
    print(f"Correlated logs with request_id {correlation_id} written to Google Cloud Logging.")
