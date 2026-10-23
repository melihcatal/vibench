import os
from typing import Any, Dict, Optional

import boto3

from security_models import SecretRequest, SecretResponse, normalize_secret_string


def get_secrets_manager_client(region_name: Optional[str] = None):
    return boto3.client("secretsmanager", region_name=region_name or os.environ.get("AWS_REGION") or os.environ.get("AWS_DEFAULT_REGION"))


def load_secret_request(secret_id: str, version_stage: Optional[str] = None, version_id: Optional[str] = None) -> SecretRequest:
    return SecretRequest(secret_id=secret_id, version_stage=version_stage, version_id=version_id)


def fetch_secret(request: SecretRequest, region_name: Optional[str] = None) -> SecretResponse:
    client = get_secrets_manager_client(region_name)
    params: Dict[str, Any] = {"SecretId": request.secret_id}
    if request.version_stage:
        params["VersionStage"] = request.version_stage
    if request.version_id:
        params["VersionId"] = request.version_id
    result = client.get_secret_value(**params)
    return SecretResponse(
        secret_id=request.secret_id,
        secret_string=normalize_secret_string(result.get("SecretString") or result.get("SecretBinary")),
        version_id=result.get("VersionId"),
        version_stage=(request.version_stage or (result.get("VersionStages") or [None])[0]),
    )
