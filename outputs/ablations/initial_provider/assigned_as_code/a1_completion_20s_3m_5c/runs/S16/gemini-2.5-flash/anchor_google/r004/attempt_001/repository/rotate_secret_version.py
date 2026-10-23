from google.cloud import secretmanager
from security_client import get_secret_manager_client
from security_models import SecretPayload

def rotate_secret_version(payload: SecretPayload):
    client = get_secret_manager_client()
    # Access a specific version or staged value
    # In Google Cloud Secret Manager, staged values are typically 'latest' or numeric versions.
    # For a true 'rotation' function, one would typically add a new secret version.
    # This function demonstrates reading a specific version as per the prompt.
    name = f"projects/{payload.project_id}/secrets/{payload.secret_id}/versions/{payload.version_id}"
    response = client.access_secret_version(request={"name": name})
    version_value = response.payload.data.decode("utf-8")
    return {"secret_version_value": version_value, "version_id": payload.version_id}
