from __future__ import annotations

from security_client import build_secret_name, get_secrets_manager_client
from security_models import SecretValue, normalize_secret_string


ROTATION_SECRET_NAME = build_secret_name("service/rotating_token")


def read_secret_version(secret_id: str = ROTATION_SECRET_NAME, version_stage: str = "AWSPENDING") -> SecretValue:
    client = get_secrets_manager_client()
    response = client.get_secret_value(SecretId=secret_id, VersionStage=version_stage)
    return SecretValue(
        secret_id=secret_id,
        version_id=response.get("VersionId", version_stage),
        value=normalize_secret_string(response["SecretString"]),
        metadata={
            "requested_stage": version_stage,
            "resolved_stages": response.get("VersionStages", []),
            "provider": "aws-secrets-manager",
        },
    )
