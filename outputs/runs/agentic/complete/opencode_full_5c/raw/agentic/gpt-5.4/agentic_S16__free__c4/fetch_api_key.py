from __future__ import annotations

from security_client import access_secret_version, get_default_locator
from security_models import SecretPayload


def fetch_api_key(secret_id: str, version_id: str = "latest") -> SecretPayload:
    locator = get_default_locator(secret_id=secret_id, version_id=version_id)
    response = access_secret_version(locator)
    value = response.payload.data.decode("utf-8")
    return SecretPayload(name=locator.resource_name(), value=value)
