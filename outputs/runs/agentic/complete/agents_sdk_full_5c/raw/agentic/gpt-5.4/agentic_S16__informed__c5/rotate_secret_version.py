from __future__ import annotations

from typing import Optional

from security_client import decode_secret_value, get_secrets_manager_client, require_secret_id
from security_models import SecretFetchRequest, normalize_secret_response


DEFAULT_STAGE = "AWSCURRENT"


def read_secret_version(version_id: Optional[str] = None, version_stage: Optional[str] = None) -> dict:
    secret_id = require_secret_id("ROTATION_SECRET_ID")
    request = SecretFetchRequest(secret_id=secret_id, version_id=version_id, version_stage=version_stage or DEFAULT_STAGE)
    client = get_secrets_manager_client()

    params = {"SecretId": request.secret_id}
    if request.version_id:
        params["VersionId"] = request.version_id
    if request.version_stage:
        params["VersionStage"] = request.version_stage

    response = client.get_secret_value(**params)
    payload = normalize_secret_response(secret_id, response, decode_secret_value(response))
    return payload.as_dict()
