import os
from google.cloud import secretmanager
from security_models import SecretResponse


def rotation_summary(secret_id: str, project_id: str = None) -> dict:
    """
    Summarize secret rotation status from Google Cloud Secret Manager.
    
    Args:
        secret_id: The secret identifier (e.g., "my-secret").
        project_id: Google Cloud project ID. Defaults to GOOGLE_CLOUD_PROJECT env var.
    
    Returns:
        A dictionary summarizing rotation status (e.g., {"versions": [...], "latest": "..."}).
    """
    if project_id is None:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    
    client = secretmanager.SecretManagerServiceClient()
    parent = f"projects/{project_id}/secrets/{secret_id}"
    
    versions = []
    for version in client.list_secret_versions(request={"parent": parent}):
        versions.append({
            "name": version.name,
            "state": version.state.name,
            "create_time": version.create_time.isoformat()
        })
    
    latest_version = client.get_secret_version(request={"name": f"{parent}/versions/latest"})
    
    return {
        "secret_id": secret_id,
        "versions": versions,
        "latest_version": latest_version.name
    }