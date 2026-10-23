from google.cloud import secretmanager
from datetime import datetime, timezone

def summarize_secret_rotation_status(project_id: str) -> dict:
    """
    Summarizes secret rotation status for secrets in a given project.
    This example lists secrets and their creation times as a proxy for rotation status.
    A real implementation would check rotation policies and last rotated timestamps.
    """
    client = secretmanager.SecretManagerServiceClient()
    parent = f"projects/{project_id}"
    secrets_summary = []

    for secret in client.list_secrets(request={"parent": parent}):
        create_time = secret.create_time.astimezone(timezone.utc) if secret.create_time else "N/A"
        secrets_summary.append({
            "secret_id": secret.secret_id,
            "name": secret.name,
            "create_time": str(create_time),
            "labels": secret.labels
        })
    return {"secret_rotation_summary": secrets_summary}
