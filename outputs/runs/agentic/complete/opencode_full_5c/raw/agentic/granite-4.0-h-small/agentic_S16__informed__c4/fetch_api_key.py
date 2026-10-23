import os
from google.cloud import secretmanager


def fetch_api_key(project_id: str, secret_id: str) -> str:
    """Fetch an API key from Google Cloud Secret Manager.

    Args:
        project_id (str): Google Cloud project identifier.
        secret_id (str): Secret ID for the API key.

    Returns:
        str: The retrieved API key value.
    """
    # Set up client using default credentials (GOOGLE_APPLICATION_CREDENTIALS)
    client = secretmanager.SecretManagerServiceClient()
    # Construct the full secret name
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    # Call the API to access the secret
    response = client.access_secret_version(name=name)
    # Return the payload as a string
    return response.payload.data.decode("UTF-8")
