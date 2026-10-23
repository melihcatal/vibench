"""
Local client helper for Google Cloud Logging.
"""
import os
from google.cloud import logging_v2

_client = None

def get_logging_client():
    """
    Initializes and returns a singleton Google Cloud Logging client.

    Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set.
    """
    global _client
    if _client is None:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        _client = logging_v2.Client(project=project_id)
    return _client
