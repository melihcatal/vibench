from __future__ import annotations

from security_client import SecretManagementConfig
from security_models import RotationStatus
from google.cloud import secretmanager



def rotation_summary(project_id: str, secret_id: str) -> RotationStatus:
    client = secretmanager.SecretManagerServiceClient()
    config = SecretManagementConfig(project_id=project_id, secret_id=secret_id, version_id="latest")
    secret = client.get_secret(request={"name": f"projects/{config.project_id}/secrets/{config.secret_id}"})
    latest = client.access_secret_version(request={"name": config.resource_name})
    state = latest.name.split("/")[-1]
    notes = f"replication={secret.replication.automatic.__class__.__name__ if secret.replication.automatic else 'user-managed'}"
    return RotationStatus(
        secret_name=secret.name,
        current_version=state,
        state="ENABLED",
        labels=dict(secret.labels),
        notes=notes,
    )
