from google.cloud import secretmanager
from typing import Dict, List
import os


def rotation_summary(project_id: str, secret_id: str) -> Dict[str, str]:
    """
    Summarizes secret rotation status from Google Cloud Secret Manager.

    Args:
        project_id: Google Cloud project ID.
        secret_id: ID of the secret to summarize.

    Returns:
        A dictionary containing rotation status, current version, and previous version.
    """
    client = secretmanager.SecretManagerServiceClient()
    secret_name = f"projects/{project_id}/secrets/{secret_id}"

    # Get current and previous versions
    versions = list(client.list_secret_versions(request={"parent": secret_name}))
    versions.sort(key=lambda x: x.create_time, reverse=True)

    current_version = versions[0].name.split("/")[-1] if versions else "unknown"
    previous_version = versions[1].name.split("/")[-1] if len(versions) > 1 else None

    return {
        "secret_id": secret_id,
        "current_version": current_version,
        "previous_version": previous_version,
        "rotation_status": "rotated" if previous_version else "never_rotated",
    }
