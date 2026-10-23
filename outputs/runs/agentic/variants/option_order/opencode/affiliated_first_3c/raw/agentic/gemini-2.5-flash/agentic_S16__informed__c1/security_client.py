from google.cloud import secretmanager
import os


def get_secret_manager_client():
    """Returns a Google Secret Manager client."""
    return secretmanager.SecretManagerServiceClient()


def access_secret_version(
    project_id: str, secret_id: str, version_id: str = "latest"
) -> str:
    """Access the payload for the given secret version.S"""
    client = get_secret_manager_client()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")
