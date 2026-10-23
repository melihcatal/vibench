from google.cloud import secretmanager
import os


def get_secret_manager_client():
    """Returns a Google Secret Manager client instance."""
    return secretmanager.SecretManagerServiceClient()


def get_project_id() -> str:
    """Retrieves the Google Cloud Project ID from environment variables."""
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT_ID")
    if not project_id:
        raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")
    return project_id
