from __future__ import annotations

from security_client import parse_secret_payload, safe_get_secret
from security_models import SecretRequest, SecretResponse

# AWS Secrets Manager integration
SECRET_ID = "app/database/connection"


def fetch_db_secret() -> SecretResponse:
    req = SecretRequest(secret_id=SECRET_ID, version_stage="AWSCURRENT")
    response = safe_get_secret(req.secret_id, version_stage=req.version_stage)
    return SecretResponse(
        secret_id=req.secret_id,
        payload=parse_secret_payload(response),
        version_id=response.get("VersionId"),
        version_stages=list(response.get("VersionStages", [])),
        metadata={"engine": "postgresql", "arn": response.get("ARN")},
    )
