from __future__ import annotations

from security_client import normalize_secret_response, safe_get_secret
from security_models import RotationSummary, SecretRequest

# AWS Secrets Manager integration
SECRET_ID = "app/rotating/secret"


def rotate_secret_version(version_stage: str = "AWSPREVIOUS") -> RotationSummary:
    req = SecretRequest(secret_id=SECRET_ID, version_stage=version_stage)
    response = safe_get_secret(req.secret_id, version_stage=req.version_stage)
    normalized = normalize_secret_response(response)
    return RotationSummary(
        secret_id=req.secret_id,
        current_version=normalized.get("version_id"),
        previous_version=response.get("VersionId"),
        labels=list(normalized.get("stages", [])),
    )
