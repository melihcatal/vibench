from __future__ import annotations

from security_client import SecretManagementConfig, access_secret_version
from security_models import SecretPayload, decode_secret_bytes



def fetch_api_key(project_id: str, secret_id: str, version_id: str = "latest") -> SecretPayload:
    config = SecretManagementConfig(project_id=project_id, secret_id=secret_id, version_id=version_id)
    response = access_secret_version(config.resource_name)
    data = decode_secret_bytes(response.payload.data)
    version_name = response.name.rsplit("/", 1)[-1]
    return SecretPayload(name=response.name, data=data, version_id=version_name)
