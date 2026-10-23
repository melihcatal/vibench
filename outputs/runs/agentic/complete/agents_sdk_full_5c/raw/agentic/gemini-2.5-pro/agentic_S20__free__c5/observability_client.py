import os
import google.cloud.logging
from google.cloud.logging_v2.client import Client as LoggingClient
from google.api_core.exceptions import GoogleAPICallError

def get_gcp_logging_client() -> LoggingClient:
    """
    Initializes and returns a Google Cloud Logging client.

    Assumes that the GOOGLE_APPLICATION_CREDENTIALS environment variable
    is set, or that the application is running in a GCP environment
    with appropriate service account permissions.

    Returns:
        A configured Google Cloud Logging client.
    
    Raises:
        Exception: If the client cannot be initialized.
    """
    try:
        project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
        client = google.cloud.logging.Client(project=project_id)
        return client
    except GoogleAPICallError as e:
        print(f"Failed to initialize Google Cloud Logging client: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred during client initialization: {e}")
        raise

def get_logger(client: LoggingClient, name: str = "app_logger"):
    """
    Retrieves a logger instance associated with the client.

    Args:
        client: The Google Cloud Logging client.
        name: The name of the logger.

    Returns:
        A logger instance.
    """
    return client.logger(name)
