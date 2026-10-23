import os
from google.cloud import secretmanager

def get_secret_manager_client():
    """Provides a configured Google Secret Manager client.
    
    This centralizes client creation for reusability.
    """
    return secretmanager.SecretManagerServiceClient()

def get_project_id() -> str:
    """Retrieves the Google Cloud project ID from environment or raises an error.
    """
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("Google Cloud project ID must be set in GOOGLE_CLOUD_PROJECT environment variable.")
    return project_id
