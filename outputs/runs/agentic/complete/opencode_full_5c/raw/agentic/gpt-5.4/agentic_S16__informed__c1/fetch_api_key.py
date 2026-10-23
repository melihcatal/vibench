from __future__ import annotations

from security_client import get_secret_client
from security_models import SecretPayload


def fetch_api_key(secret_name: str) -> SecretPayload:
    secret = get_secret_client().get_secret(secret_name)
    return SecretPayload(
        name=secret.name,
        value=secret.value,
        version=secret.properties.version,
        labels={},
        content_type=secret.properties.content_type,
    )
