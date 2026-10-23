from __future__ import annotations

from security_client import get_secrets_manager_client, require_secret_id
from security_models import normalize_secret_value


AWS_SECRETS_MANAGER_SERVICE = "secretsmanager"


def fetch_api_key(secret_id: str | None = None) -> str:
    client = get_secrets_manager_client()
    resolved_secret_id = secret_id or require_secret_id("API_KEY_SECRET_ID")
    response = client.get_secret_value(SecretId=resolved_secret_id)
    payload = normalize_secret_value(response, resolved_secret_id)
    return payload.text()
