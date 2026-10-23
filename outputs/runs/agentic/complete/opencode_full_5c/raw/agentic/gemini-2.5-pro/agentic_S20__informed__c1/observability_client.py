import os
from google.cloud import logging


def get_logging_client():
    """Initializes and returns a Google Cloud Logging client."""
    # Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    return logging.Client()
