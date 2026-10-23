import os
from google.cloud import logging


def get_logging_client():
    """
    Initializes and returns a Google Cloud Logging client.
    Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    """
    return logging.Client()


def get_log_name():
    """
    Returns the log name from an environment variable.
    """
    return os.environ.get("GCP_LOG_NAME", "my-application-log")
