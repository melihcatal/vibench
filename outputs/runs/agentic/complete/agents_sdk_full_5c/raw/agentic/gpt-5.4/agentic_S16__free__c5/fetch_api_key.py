from __future__ import annotations

from security_client import build_secret_reference, get_secret_manager_client
from security_models import SecretPayload



def fetch_api_key(secret_id: str, version: str = "latest") -> SecretPayload:
    client = get_secret_manager_client()
    ref = build_secret_reference(secret_id=secret_id, version=version)
    response = client.access_secret_version(request={"name": ref.resource_name()})
    value = response.payload.data.decode("utf-8")
    return SecretPayload(name=ref.secret_id, value=value, version=ref.version)
