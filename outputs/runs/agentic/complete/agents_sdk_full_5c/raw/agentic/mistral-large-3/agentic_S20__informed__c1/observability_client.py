import os
from google.cloud import logging as cloud_logging
from google.api_core.client_options import ClientOptions


def get_logging_client() -> cloud_logging.Client:
    """Initialize and return a Google Cloud Logging client."""
    client_options = ClientOptions(
        api_endpoint=os.getenv("GOOGLE_LOGGING_API_ENDPOINT", "logging.googleapis.com")
    )
    return cloud_logging.Client(client_options=client_options)