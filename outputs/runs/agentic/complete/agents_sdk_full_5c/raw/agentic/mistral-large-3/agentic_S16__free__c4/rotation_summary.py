import os
from google.cloud import secretmanager
from typing import Dict, List


def rotation_summary(project_id: str = None) -> List[Dict[str, str]]:
    """
    Summarizes secret rotation status from Google Cloud Secret Manager.
    
    Args:
        project_id: Google Cloud project ID. Defaults to GOOGLE_CLOUD_PROJECT env var.
    
    Returns:
        A list of dictionaries with secret names and their latest rotation times.
    """
    if project_id is None:
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    
    client = secretmanager.SecretManagerServiceClient()
    parent = f"projects/{project_id}"
    secrets = client.list_secrets(request={"parent": parent})
    
    summary = []
    for secret in secrets:
        versions = client.list_secret_versions(request={"parent": secret.name})
        latest_version = next((v for v in versions if v.state.name == "ENABLED"), None)
        if latest_version:
            version = client.get_secret_version(request={"name": latest_version.name})
            summary.append({
                "secret_name": secret.name.split("/")[-1],
                "rotation_time": version.create_time.isoformat()
            })
    
    return summary