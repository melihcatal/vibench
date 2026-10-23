from __future__ import annotations

from security_client import get_secret_client
from security_models import SecretPayload


def fetch_db_secret(secret_name: str, version: str | None = None) -> SecretPayload:
    secret = get_secret_client().get_secret(secret_name, version=version)
    return SecretPayload(
        name=secret.name,
        value=secret.value,
        version=secret.properties.version,
        labels={},
        content_type=secret.properties.content_type,
    )
