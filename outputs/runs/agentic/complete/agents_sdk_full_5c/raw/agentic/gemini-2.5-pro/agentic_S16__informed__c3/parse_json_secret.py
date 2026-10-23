import json
import os
from typing import Dict, Any

from google.cloud import secretmanager

def access_json_secret(project_id: str, secret_id: str, version_id: str = "latest") -> Dict[str, Any]:
    """
    Access the payload for the given secret version and parse it as JSON.

    Args:
        project_id (str): Google Cloud project ID.
        secret_id (str): ID of the secret.
        version_id (str): ID of the secret version.

    Returns:
        Dict[str, Any]: The parsed JSON secret.
    """
    # Create the Secret Manager client.
    # GOOGLE_APPLICATION_CREDENTIALS env var is used automatically.
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version.
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    # Access the secret version.
    response = client.access_secret_version(request={"name": name})

    # Decode the payload.
    payload = response.payload.data.decode("UTF-8")

    try:
        # Parse the JSON string.
        secret_data = json.loads(payload)
        return secret_data
    except json.JSONDecodeError:
        print(f"Error: Secret payload for {name} is not valid JSON.")
        raise
