import os
from typing import List, Dict, Any
from security_client import SecretManagerClient


def rotation_summary() -> List[Dict[str, Any]]:
    project_id = os.environ.get("GCP_PROJECT_ID")
    if not project_id:
        raise ValueError("GCP_PROJECT_ID environment variable must be set.")

    client = SecretManagerClient(project_id=project_id)
    summary = []

    for secret in client.list_secrets_with_versions():
        metadata = client.get_secret_metadata(secret.secret_id)
        summary.append(
            {
                "secret_id": secret.secret_id,
                "create_time": metadata.get("create_time"),
                "rotation_period": metadata.get("rotation_period"),
                "labels": metadata.get("labels"),
            }
        )
    return summary
