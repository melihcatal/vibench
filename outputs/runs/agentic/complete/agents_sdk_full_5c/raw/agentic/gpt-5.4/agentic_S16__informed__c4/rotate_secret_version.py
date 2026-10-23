from __future__ import annotations

from typing import Optional

from security_client import build_secrets_manager_client
from security_models import SecretFetchRequest, SecretPayload, normalize_secret_value


def read_secret_version(
    secret_id: str,
    region_name: str | None = None,
    version_id: Optional[str] = None,
    version_stage: Optional[str] = None,
) -> SecretPayload:
    request = SecretFetchRequest(secret_id=secret_id, version_id=version_id, version_stage=version_stage)
    client = build_secrets_manager_client(region_name)
    params = {"SecretId": request.secret_id}
    if request.version_id:
        params["VersionId"] = request.version_id
    if request.version_stage:
        params["VersionStage"] = request.version_stage
    response = client.get_secret_value(**params)
    return normalize_secret_value(secret_id, response)
