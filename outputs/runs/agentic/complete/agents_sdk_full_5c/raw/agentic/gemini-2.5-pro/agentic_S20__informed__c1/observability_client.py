
import os
from google.cloud import logging

def get_gcp_logging_client():
    """
    Initializes and returns a Google Cloud Logging client.
    
    Assumes that the GOOGLE_APPLICATION_CREDENTIALS environment variable
    is set to the path of a valid service account key file.
    """
    project_id = os.getenv("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")
        
    logging_client = logging.Client(project=project_id)
    return logging_client
