from google.cloud import logging

def get_logging_client():
    """Returns a Google Cloud Logging client."""
    return logging.Client()
