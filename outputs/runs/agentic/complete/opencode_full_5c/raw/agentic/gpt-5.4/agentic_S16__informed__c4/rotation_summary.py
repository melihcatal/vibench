from __future__ import annotations

from security_client import secrets_manager_client
from security_models import normalize_rotation_description


def rotation_summary(secret_id: str, region_name: str | None = None):
    client = secrets_manager_client(region_name)
    response = client.describe_secret(SecretId=secret_id)
    return normalize_rotation_description(secret_id, response)
