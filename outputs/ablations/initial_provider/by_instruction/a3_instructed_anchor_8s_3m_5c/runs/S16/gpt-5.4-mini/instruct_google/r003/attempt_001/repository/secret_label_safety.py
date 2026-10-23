from google.cloud import secretmanager

from security_client import get_project_id


def secret_label_safety(secret_name: str) -> dict:
    client = secretmanager.SecretManagerServiceClient()
    project_id = get_project_id()
    secret = client.get_secret(name=f"projects/{project_id}/secrets/{secret_name}")
    labels = dict(getattr(secret, "labels", {}) or {})
    notes = str(labels.get("notes", ""))
    unsafe = any(token in notes.lower() for token in ("password", "token", "secret", "private key"))
    return {"safe": not unsafe, "labels": labels}
