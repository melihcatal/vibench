from google.cloud import logging
from google.cloud.logging_v2 import LoggingServiceV2Client
import os

def get_logging_client() -> logging.Client:
    """
    Returns a Google Cloud Logging client.
    """
    return logging.Client()

def get_logging_service_v2_client() -> LoggingServiceV2Client:
    """
    Returns a Google Cloud Logging Service V2 client (for advanced query operations).
    """
    return LoggingServiceV2Client()

def get_project_id() -> str:
    """
    Retrieves the Google Cloud project ID from environment variables or gcloud configuration.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        # Fallback to default project from gcloud if not set as environment variable
        # In a real application, consider using google.auth.default() or explicit configuration
        try:
            import google.auth
            credentials, project_id = google.auth.default()
        except Exception:
            raise RuntimeError("Google Cloud Project ID not found. Set GOOGLE_CLOUD_PROJECT environment variable.")
    return project_id
