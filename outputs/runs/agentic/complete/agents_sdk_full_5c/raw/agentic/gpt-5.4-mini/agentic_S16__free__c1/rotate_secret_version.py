from __future__ import annotations

import os
from typing import Optional

from security_client import get_aws_secrets_manager_client, secret_id_from_env
from security_models import SecretFetchResult, normalize_secret_payload


def rotate_secret_version(secret_id: Optional[str] = None, version_stage: str = "AWSCURRENT") -> SecretFetchResult:
    """Read a specific AWS Secrets Manager version or staged value."""
    client = get_aws_secrets_manager_client()
    secret_name = secret_id or secret_id_from_env("ROTATE_SECRET_ID", "rotation/secret")
    response = client.get_secret_value(SecretId=secret_name, VersionStage=version_stage)
    payload = normalize_secret_payload(response)
    return SecretFetchResult(secret_id=secret_name, version_id=response.get("VersionId"), value=str(payload.get("value") or payload.get("secret_string") or ""), raw=payload)


if __name__ == "__main__":
    result = rotate_secret_version(os.getenv("ROTATE_SECRET_ID"), os.getenv("ROTATE_VERSION_STAGE", "AWSCURRENT"))
    print(result.value)
