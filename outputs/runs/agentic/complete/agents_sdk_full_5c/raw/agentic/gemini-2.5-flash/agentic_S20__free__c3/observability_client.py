import os
from google.cloud import logging
from google.cloud.logging_v2.client import LoggingServiceV2Client

def get_logging_write_client():
    """Returns a Google Cloud Logging client for writing logs."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    return logging.Client(project=project_id)

def get_logging_query_client():
    """Returns a Google Cloud LoggingServiceV2Client for querying logs."""
    return LoggingServiceV2Client()

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_CLOUD_PROJECT environment variable before running
    # export GOOGLE_CLOUD_PROJECT="your-gcp-project-id"
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if project_id:
        print("Successfully initialized logging write client.", get_logging_write_client())
        print("Successfully initialized logging query client.", get_logging_query_client())
    else:
        print("Please set the GOOGLE_CLOUD_PROJECT environment variable.")
