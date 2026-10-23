import os
from google.cloud import logging


def get_logging_client():
    """Returns a Google Cloud Logging client."""
    # GOOGLE_APPLICATION_CREDENTIALS environment variable should be set
    return logging.Client()
