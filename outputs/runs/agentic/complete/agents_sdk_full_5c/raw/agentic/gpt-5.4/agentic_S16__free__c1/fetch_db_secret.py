from __future__ import annotations

from security_client import SecretManagementConfig, access_secret_version
from security_models import SecretPayload, decode_secret_bytes



def fetch_db_secret(project_id: str, secret_id: str, version_id: str = "latest") -> SecretPayload:
    config = SecretManagementConfig(project_id=project_id, secret_id=secret_id, version_id=version_id)
    response = access_secret_version(config.resource_name)
    secret_text = decode_secret_bytes(response.payload.data)
    return SecretPayload(
        name=response.name,
        data=secret_text,
        version_id=response.name.split("/")[-1],
        annotations={"provider": "Google Cloud Secret Manager"},
    )
