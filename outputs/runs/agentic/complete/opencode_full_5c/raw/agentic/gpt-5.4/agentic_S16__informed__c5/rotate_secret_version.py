from __future__ import annotations

from security_client import get_secret_manager_client
from security_models import SecretRequest, normalize_secret_response


def rotate_secret_version(request: SecretRequest):
    client = get_secret_manager_client()
    params = {"SecretId": request.secret_id}
    if request.version_id:
        params["VersionId"] = request.version_id
    if request.version_stage:
        params["VersionStage"] = request.version_stage
    response = client.get_secret_value(**params)
    return normalize_secret_response(request.secret_id, response)
