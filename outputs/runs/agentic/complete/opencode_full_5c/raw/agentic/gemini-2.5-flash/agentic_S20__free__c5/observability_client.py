from google.cloud import logging_v2
from google.cloud.logging_v2.client import Client as LoggingClient


def get_logging_client() -> LoggingClient:
    """Initializes and returns a Google Cloud Logging client."""
    # Google Cloud Logging automatically uses credentials from the environment
    # (e.g., GOOGLE_APPLICATION_CREDENTIALS environment variable or default service account)
    return logging_v2.Client()
