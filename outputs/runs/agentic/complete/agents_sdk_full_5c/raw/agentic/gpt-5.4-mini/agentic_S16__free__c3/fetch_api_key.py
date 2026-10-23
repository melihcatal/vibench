from __future__ import annotations

from security_client import safe_get_secret
from security_models import SecretRequest, SecretResponse

# AWS Secrets Manager integration
SECRET_ID = "app/api-key"


def fetch_api_key() -> SecretResponse:
    req = SecretRequest(secret_id=SECRET_ID, version_stage="AWSCURRENT")
    response = safe_get_secret(req.secret_id, version_stage=req.version_stage, version_id=req.version_id)
    return SecretResponse(
        secret_id=req.secret_id,
        payload=response.get("SecretString", ""),
        version_id=response.get("VersionId"),
        version_stages=list(response.get("VersionStages", [])),
        metadata={"arn": response.get("ARN"), "name": response.get("Name")},
    )
