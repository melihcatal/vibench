import os
from google.cloud import secretmanager

from security_client import get_gcp_secret_manager_client


def rotate_secret_version(secret_id: str, version_id: str = "1") -> str:
    """
    Reads a specific, non-latest version of a secret from Google Secret Manager.

    This is useful in rotation schemes to access a previous or specific staged version.
    """
    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable not set.")

    client = get_gcp_secret_manager_client()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    try:
        response = client.access_secret_version(name=name)
        payload = response.payload.data.decode("UTF-8")
        return payload
    except Exception as e:
        print(f"Error accessing secret version: {e}")
        raise
