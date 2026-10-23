from google.cloud import logging_v2

def get_logging_client():
    """Initializes and returns a Google Cloud Logging client."""
    return logging_v2.LoggingServiceV2Client()

def get_query_client():
    """Initializes and returns a Google Cloud Logging client for querying."""
    # For this service, the same client is used for writing and reading.
    return logging_v2.LoggingServiceV2Client()
