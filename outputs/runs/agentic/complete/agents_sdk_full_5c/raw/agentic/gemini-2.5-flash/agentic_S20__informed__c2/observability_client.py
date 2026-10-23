import os
from google.cloud import logging

def get_logging_client():
    """Initializes and returns a Google Cloud Logging client."""
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    # or the client will use default credentials from the environment.
    return logging.Client()

def get_project_id():
    """Returns the Google Cloud Project ID."""
    # You might want to get this from an environment variable or explicit config
    return os.getenv("GOOGLE_CLOUD_PROJECT", "your-gcp-project-id")
