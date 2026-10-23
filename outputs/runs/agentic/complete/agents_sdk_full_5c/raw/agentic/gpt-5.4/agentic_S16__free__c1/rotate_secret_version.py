from __future__ import annotations

from typing import Optional

from google.cloud import secretmanager

from security_models import SecretPayload, decode_secret_bytes



def read_secret_version(project_id: str, secret_id: str, version_id: str = "latest") -> SecretPayload:
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
    response = client.access_secret_version(request={"name": name})
    return SecretPayload(name=response.name, data=decode_secret_bytes(response.payload.data), version_id=version_id)



def read_secret_by_alias(project_id: str, secret_id: str, alias: Optional[str] = None) -> SecretPayload:
    target_version = alias or "latest"
    return read_secret_version(project_id=project_id, secret_id=secret_id, version_id=target_version)
