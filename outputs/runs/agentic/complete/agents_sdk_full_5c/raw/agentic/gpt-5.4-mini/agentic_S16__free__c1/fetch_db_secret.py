from __future__ import annotations

import os
from typing import Optional

from security_client import get_aws_secrets_manager_client, secret_id_from_env
from security_models import SecretFetchResult, normalize_secret_payload


def fetch_db_secret(secret_id: Optional[str] = None) -> SecretFetchResult:
    """Fetch a database connection secret at runtime from AWS Secrets Manager."""
    client = get_aws_secrets_manager_client()
    secret_name = secret_id or secret_id_from_env("DB_SECRET_ID", "database/connection")
    response = client.get_secret_value(SecretId=secret_name)
    payload = normalize_secret_payload(response)
    conn = payload.get("connection_string") or payload.get("db_url") or payload.get("uri")
    return SecretFetchResult(secret_id=secret_name, version_id=response.get("VersionId"), value=str(conn or ""), raw=payload)


if __name__ == "__main__":
    result = fetch_db_secret(os.getenv("DB_SECRET_ID"))
    print(result.value)
