from __future__ import annotations

import os
from typing import Optional

from security_client import get_aws_secrets_manager_client, secret_id_from_env
from security_models import SecretFetchResult, normalize_secret_payload


def fetch_api_key(secret_id: Optional[str] = None) -> SecretFetchResult:
    """Fetch an API key from AWS Secrets Manager."""
    client = get_aws_secrets_manager_client()
    secret_name = secret_id or secret_id_from_env("API_KEY_SECRET_ID", "api/key")
    response = client.get_secret_value(SecretId=secret_name)
    payload = normalize_secret_payload(response)
    api_key = payload.get("api_key") or payload.get("key") or payload.get("token") or payload.get("value")
    return SecretFetchResult(secret_id=secret_name, version_id=response.get("VersionId"), value=str(api_key or ""), raw=payload)


if __name__ == "__main__":
    result = fetch_api_key(os.getenv("API_KEY_SECRET_ID"))
    print(result.value)
