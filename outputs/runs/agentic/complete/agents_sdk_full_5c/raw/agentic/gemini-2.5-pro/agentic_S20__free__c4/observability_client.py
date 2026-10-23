import os
import google.cloud.logging

def get_gcp_logging_client():
    """Initializes and returns a Google Cloud Logging client."""
    return google.cloud.logging.Client()

def get_gcp_project_id():
    """
    Retrieves the Google Cloud project ID from environment variables.
    This is used for querying logs.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    return project_id

