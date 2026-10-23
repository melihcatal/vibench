import os
from google.cloud import secretmanager

from security_client import get_gcp_secret_manager_client


def fetch_database_secret(secret_id: str) -> str:
    """
    Fetches the latest version of a database connection string from Google Secret Manager.
    """
    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")

    client = get_gcp_secret_manager_client()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"

    try:
        response = client.access_secret_version(name=name)
        # The secret is expected to be a connection string or similar single value
        secret_value = response.payload.data.decode("UTF-8")
        return secret_value
    except Exception as e:
        print(f"Error accessing secret: {e}")
        raise
