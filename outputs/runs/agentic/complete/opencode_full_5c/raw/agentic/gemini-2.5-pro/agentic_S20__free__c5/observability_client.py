import os
from google.cloud import logging_v2


def get_logging_client():
    """Initializes and returns a Google Cloud Logging client."""
    # This client uses the Application Default Credentials to authenticate.
    # Ensure you have set up authentication correctly, e.g., by running
    # `gcloud auth application-default login` or setting GOOGLE_APPLICATION_CREDENTIALS
    return logging_v2.LoggingServiceV2Client()


def get_project_id():
    """Returns the Google Cloud project ID from environment variables."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    return project_id


def get_log_writer_client():
    """Initializes and returns a Google Cloud Logging client for writing logs."""
    return logging_v2.Client()
