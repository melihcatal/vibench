from google.cloud import logging as gcp_logging
from google.cloud import logging_v2
import os

def get_logging_client():
    """Returns a Google Cloud Logging Client instance for writing logs."""
    # The client automatically uses GOOGLE_APPLICATION_CREDENTIALS or default credentials
    return gcp_logging.Client()

def get_logging_v2_client(project_id: str):
    """Returns a Google Cloud Logging V2 Client instance for reading/querying logs."""
    # The client automatically uses GOOGLE_APPLICATION_CREDENTIALS or default credentials
    # The project_id is needed for constructing the resource name for list_entries calls.
    return logging_v2.Client(project=project_id)

def get_project_id() -> str:
    """Fetches the Google Cloud project ID from the environment variable GOOGLE_CLOUD_PROJECT.
    Raises ValueError if not set.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set. Please set it to your GCP project ID.")
    return project_id
