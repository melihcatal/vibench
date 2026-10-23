from google.cloud import logging
import os
import json

def write_structured_log(message: str, severity: str = "INFO", component: str = "example-app"):
    client = logging.Client()
    logger = client.logger("application-logs")

    log_entry = {
        "message": message,
        "severity": severity,
        "component": component,
        "environment": os.getenv("ENVIRONMENT", "development")
    }
    logger.log_struct(log_entry)

if __name__ == "__main__":
    write_structured_log("User login successful", "INFO", "auth-service")
    print("Structured log written to Google Cloud Logging.")
