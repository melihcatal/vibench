import json
from typing import Optional, Dict, Any
from security_client import get_gcp_secret_manager_client

def get_json_secret_from_gcp(project_id: str, secret_id: str, version_id: str = "latest") -> Optional[Dict[str, Any]]:
    """
    Retrieves a secret from Google Cloud Secret Manager and parses it as JSON.

    Args:
        project_id: The Google Cloud project ID.
        secret_id: The ID of the secret.
        version_id: The version of the secret.

    Returns:
        A dictionary parsed from the secret's JSON payload, or None.
    """
    client = get_gcp_secret_manager_client()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"

    try:
        response = client.access_secret_version(request={"name": name})
        payload = response.payload.data.decode("UTF-8")
        return json.loads(payload)
    except Exception:
        # Broad exception for simplicity, could be more granular (e.g., GRPC errors)
        return None
