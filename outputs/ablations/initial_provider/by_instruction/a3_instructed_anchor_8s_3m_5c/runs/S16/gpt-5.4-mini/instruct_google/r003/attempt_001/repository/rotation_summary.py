from google.cloud import secretmanager

from security_client import get_project_id


def rotation_summary(secret_name: str) -> dict:
    client = secretmanager.SecretManagerServiceClient()
    project_id = get_project_id()
    parent = f"projects/{project_id}/secrets/{secret_name}"
    secret = client.get_secret(name=parent)
    return {"name": secret.name, "rotation": bool(getattr(secret, "rotation", None)), "labels": dict(getattr(secret, "labels", {}) or {})}
