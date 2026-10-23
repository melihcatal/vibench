from __future__ import annotations

from security_client import secrets_manager_client
from security_models import SecretRequest, normalize_secret_value


def rotate_secret_version(request: SecretRequest, region_name: str | None = None):
    client = secrets_manager_client(region_name)
    params = {"SecretId": request.secret_id}
    if request.version_id:
        params["VersionId"] = request.version_id
    if request.version_stage:
        params["VersionStage"] = request.version_stage
    response = client.get_secret_value(**params)
    return normalize_secret_value(request.secret_id, response)
