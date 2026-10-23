import os
from google.cloud import secretmanager

def get_secret_manager_client():
    """
    Provides a configured Google Secret Manager client.
    Assumes GOOGLE_APPLICATION_CREDENTIALS environment variable is set
    or runs in an authenticated GCP environment.
    """
    return secretmanager.SecretManagerServiceClient()

def get_project_id() -> str:
    """
    Retrieves the Google Cloud project ID from environment variables.
    """
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT environment variable not set.")
    return project_id
