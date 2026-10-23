from __future__ import annotations

from typing import Dict, Any, Optional

from security_client import (
    get_secrets_manager_client,
    optional_version_id,
    optional_version_stage,
    require_secret_id,
)
from security_models import normalize_secret_value


AWS_SECRETS_MANAGER_SERVICE = "secretsmanager"
DEFAULT_STAGE = "AWSCURRENT"


def read_secret_version(
    secret_id: str | None = None,
    version_id: Optional[str] = None,
    version_stage: Optional[str] = None,
) -> Dict[str, Any]:
    client = get_secrets_manager_client()
    resolved_secret_id = secret_id or require_secret_id("ROTATION_SECRET_ID")
    request: Dict[str, Any] = {"SecretId": resolved_secret_id}

    resolved_version_id = version_id or optional_version_id()
    resolved_version_stage = version_stage or optional_version_stage(default=DEFAULT_STAGE)

    if resolved_version_id:
        request["VersionId"] = resolved_version_id
    elif resolved_version_stage:
        request["VersionStage"] = resolved_version_stage

    response = client.get_secret_value(**request)
    payload = normalize_secret_value(response, resolved_secret_id)
    return {
        "secret_id": payload.secret_id,
        "version_id": payload.version_id,
        "version_stages": payload.version_stages,
        "value": payload.text(),
    }
