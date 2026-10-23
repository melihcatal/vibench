from google.cloud import kms_v1
from functools import lru_cache
import os

@lru_cache(maxsize=1)
def get_kms_client() -> kms_v1.KeyManagementServiceClient:
    """Returns a cached Google Cloud KMS client."""
    # Credentials will be picked up from the environment (e.g., GOOGLE_APPLICATION_CREDENTIALS)
    return kms_v1.KeyManagementServiceClient()

# Example of how to get project ID from environment variables
def get_gcp_project_id() -> str:
    """Retrieves the Google Cloud Project ID from environment variables."""
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        project_id = os.getenv("GCP_PROJECT") # Common alternative
    if not project_id:
        raise ValueError("Google Cloud Project ID not found in environment variables (GOOGLE_CLOUD_PROJECT or GCP_PROJECT).")
    return project_id
