
import os
from functools import lru_cache

from google.cloud import monitoring_v3


@lru_cache(maxsize=1)
def get_monitoring_client() -> monitoring_v3.MetricServiceClient:
    """
    Initializes and returns a GCP Monitoring MetricServiceClient.

    Uses LRU cache to ensure the client is a singleton.
    Credentials are automatically handled by the Google Cloud client library
    based on the environment (e.g., GOOGLE_APPLICATION_CREDENTIALS).
    """
    return monitoring_v3.MetricServiceClient()


def get_gcp_project_id() -> str:
    """
    Retrieves the GCP project ID from an environment variable.
    
    Raises:
        ValueError: If the environment variable is not set.

    Returns:
        The GCP project ID string.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("The GOOGLE_CLOUD_PROJECT environment variable must be set.")
    return project_id
