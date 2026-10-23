from google.cloud import logging as google_logging
import os


def get_logging_client():
    """
    Initializes and returns a Google Cloud Logging client.

    Assumes that the 'GOOGLE_APPLICATION_CREDENTIALS' environment variable
    is set to the path of a valid service account key file.

    Returns:
        google_logging.Client: An instance of the Google Cloud Logging client.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    client = google_logging.Client(project=project_id)
    return client
