import os
from google.cloud import logging

# --- Client Configuration ---

# It's recommended to manage the project ID via environment variables
# for portability between different environments (dev, staging, prod).
GCP_PROJECT_ID = os.environ.get("GCP_PROJECT_ID")

_gcp_logging_client = None


def get_gcp_logging_client() -> logging.Client:
    """
    Initializes and returns a singleton Google Cloud Logging client.

    This function ensures that the client is instantiated only once and re-used
    across the application, which is a best practice for efficiency.

    It requires the GCP_PROJECT_ID environment variable to be set.

    Returns:
        An instance of google.cloud.logging.Client.

    Raises:
        ValueError: If the GCP_PROJECT_ID environment variable is not set.
    """
    global _gcp_logging_client
    
    if _gcp_logging_client is None:
        if not GCP_PROJECT_ID:
            raise ValueError("GCP_PROJECT_ID environment variable not set.")
        
        # Initializes the client. Application Default Credentials are used
        # by default, which is suitable for most environments (local, GCE, GKE).
        _gcp_logging_client = logging.Client(project=GCP_PROJECT_ID)

    return _gcp_logging_client
