from google.cloud import logging


def get_logging_client():
    """Initializes and returns a Google Cloud Logging client."""
    return logging.Client()
