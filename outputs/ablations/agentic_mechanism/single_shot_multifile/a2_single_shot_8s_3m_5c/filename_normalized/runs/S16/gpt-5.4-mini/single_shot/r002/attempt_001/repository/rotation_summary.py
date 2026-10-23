from typing import Dict, List

from google.cloud import secretmanager

from security_client import load_config


def rotation_summary(secret_name: str) -> Dict[str, List[str]]:
    config = load_config()
    client = secretmanager.SecretManagerServiceClient()
    parent = f"projects/{config.project_id}/secrets/{secret_name}"
    versions = client.list_secret_versions(request={"parent": parent})
    status = []
    for version in versions:
        status.append(f"{version.name}:{version.state.name}")
    return {"secret_name": secret_name, "versions": status}
