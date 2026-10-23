import os
import json
from google.cloud import secretmanager

def parse_json_secret(secret_id: str, project_id: str = None) -> dict:
    """Retrieves and parses a JSON-formatted secret from Google Secret Manager.
    
    Args:
        secret_id: The ID of the secret to fetch.
        project_id: The Google Cloud project ID. If None, it will be inferred.
    
    Returns:
        The parsed JSON secret as a dictionary.
    
    Raises:
        json.JSONDecodeError: If the secret content is not valid JSON.
    """
    if project_id is None:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

    if not project_id:
        raise ValueError("Google Cloud project ID must be provided or set in GOOGLE_CLOUD_PROJECT environment variable.")

    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    
    response = client.access_secret_version(request={"name": name})
    secret_payload = response.payload.data.decode("UTF-8")
    
    return json.loads(secret_payload)

if __name__ == "__main__":
    # Example usage:
    # Set GOOGLE_CLOUD_PROJECT environment variable or pass project_id
    # secret_id = "my-json-config-secret"
    # json_secret = parse_json_secret(secret_id)
    # print(f"Parsed JSON Secret: {json_secret}")
    pass
