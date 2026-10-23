import json
from google.cloud import secretmanager
from security_models import SecretPayloadModel

def summarize_rotation(project_id: str, secret_id: str) -> dict:
    """Summarizes the rotation status of a secret.

    The function reads the latest version and the last rotated (staged)
    version from Google Secret Manager, extracts key metadata, and returns
    a concise summary as a dict.

    Args:
        project_id (str): GCP project ID.
        secret_id (str): Secret name.

    Returns:
        dict: Summary containing:
            - latest_version: version number of the active secret
            - latest_payload: decrypted payload of latest version
            - staged_version: version number of the staged (rotated) secret
            - staged_payload: decrypted payload of the staged secret (if any)
    """
    client = secretmanager.SecretManagerServiceClient()
    latest_name = f"projects/{project_id}/secrets/{secret_id}/versions/latest"
    latest_resp = client.access_secret_version(name=latest_name)
    latest_payload = latest_resp.payload.data.decode('UTF-8')
    latest_payload_obj = json.loads(latest_payload)

    # Attempt to fetch the staged version; if it does not exist, return None
    try:
        staged_name = f"projects/{project_id}/secrets/{secret_id}/versions/staged"
        staged_resp = client.access_secret_version(name=staged_name)
        staged_payload = staged_resp.payload.data.decode('UTF-8')
        staged_payload_obj = json.loads(staged_payload)
    except Exception:
        staged_payload_obj = None

    # Build summary
    summary = {
        'latest_version': 'latest',
        'latest_payload': latest_payload_obj,
        'staged_version': 'staged' if staged_payload_obj else None,
        'staged_payload': staged_payload_obj,
    }
    return summary
