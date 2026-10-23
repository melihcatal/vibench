from __future__ import annotations

from typing import Optional

from security_client import get_secrets_manager_client
from security_models import SecretRequest, normalize_secret_response


def rotate_secret_version(
    secret_id: str,
    version_id: Optional[str] = None,
    version_stage: Optional[str] = None,
):
    request = SecretRequest(
        secret_id=secret_id, version_id=version_id, version_stage=version_stage
    )
    client = get_secrets_manager_client()
    params = {"SecretId": request.secret_id}
    if request.version_id:
        params["VersionId"] = request.version_id
    if request.version_stage:
        params["VersionStage"] = request.version_stage
    response = client.get_secret_value(**params)
    return normalize_secret_response(secret_id, response)
