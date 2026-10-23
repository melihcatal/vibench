import os
import json
from google.cloud import secretmanager

from security_models import ParsedJSONSecret, SecretFetchError

def get_json_secret(project_id: str, secret_id: str, version_id: str = "latest") -> ParsedJSONSecret:
    """
    Retrieves and parses a JSON-formatted secret from Google Cloud Secret Manager.

    Args:
        project_id: The Google Cloud project ID.
        secret_id: The ID of the secret.
        version_id: The version of the secret to access.

    Returns:
        A Pydantic model with the parsed secret data.
    
    Raises:
        SecretFetchError: If the secret cannot be fetched or parsed.
    """
    try:
        client = secretmanager.SecretManagerServiceClient()
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
        
        response = client.access_secret_version(request={"name": name})
        
        payload = response.payload.data.decode("UTF-8")
        secret_data = json.loads(payload)
        
        return ParsedJSONSecret(**secret_data)
    except json.JSONDecodeError as e:
        raise SecretFetchError(f"Failed to parse JSON for secret '{secret_id}': {e}")
    except Exception as e:
        raise SecretFetchError(f"Failed to retrieve secret '{secret_id}' from GCP: {e}")

