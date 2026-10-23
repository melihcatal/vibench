import os
from google.cloud import logging as google_logging


def get_logging_client():
    """
    Initializes and returns a Google Cloud Logging client.

    Assumes that the GOOGLE_APPLICATION_CREDENTIALS environment variable
    is set.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")

    client = google_logging.Client(project=project_id)
    return client
