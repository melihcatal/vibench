import os
import google.cloud.logging
from google.cloud import logging_v2

def get_logging_client() -> google.cloud.logging.Client:
    """Provides a Google Cloud Logging client instance."""
    return google.cloud.logging.Client()

def get_logging_service_v2_client() -> logging_v2.LoggingServiceV2Client:
    """Provides a Google Cloud Logging Service V2 client instance for advanced queries."""
    return logging_v2.LoggingServiceV2Client()

def get_gcp_project_id() -> str:
    """Retrieves the GCP project ID from environment variables or default settings."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        # Fallback to default project from credentials if not explicitly set
        try:
            import google.auth
            credentials, project_id = google.auth.default()
        except Exception:
            pass # Will return None or raise error later if not found
    return project_id
