import os
from google.cloud import logging

# Google Cloud Logging credentials are expected via the standard env var
# GOOGLE_APPLICATION_CREDENTIALS

def get_logging_client() -> logging.Client:
    """Create and return a Google Cloud Logging client.

    The client reads credentials from the environment variable
    GOOGLE_APPLICATION_CREDENTIALS, which should point at a service account JSON.
    """
    return logging.Client()

if __name__ == "__main__":
    # Demonstrative usage
    client = get_logging_client()
    logger = client.logger("projects/your-project-id/logs/app-logs")
    logger.log_struct({"message": "Client initialized", "severity": "INFO"})
