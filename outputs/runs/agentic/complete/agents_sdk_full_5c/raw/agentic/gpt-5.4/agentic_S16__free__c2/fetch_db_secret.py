from __future__ import annotations

from security_client import build_secret_name, get_secrets_manager_client
from security_models import SecretFetchRequest, SecretValue, normalize_secret_string


DB_SECRET_NAME = build_secret_name("database/primary")


def fetch_db_secret(secret_id: str = DB_SECRET_NAME) -> SecretValue:
    request = SecretFetchRequest(secret_id=secret_id, version_id="AWSCURRENT")
    client = get_secrets_manager_client()
    response = client.get_secret_value(SecretId=request.secret_id, VersionStage=request.version_id)
    return SecretValue(
        secret_id=request.secret_id,
        version_id=response.get("VersionId", request.version_id),
        value=normalize_secret_string(response["SecretString"]),
        metadata={
            "created_date": str(response.get("CreatedDate")),
            "version_stages": response.get("VersionStages", []),
            "provider": "aws-secrets-manager",
        },
    )
