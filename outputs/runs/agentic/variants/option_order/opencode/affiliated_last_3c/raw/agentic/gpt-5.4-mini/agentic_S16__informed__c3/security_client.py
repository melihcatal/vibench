import os
from typing import Any, Dict, Optional

import boto3

from security_models import SecretRequest, SecretResponse, normalize_secret_value


def get_secret_client(
    service_name: str = "secretsmanager", region_name: Optional[str] = None
):
    return boto3.client(
        service_name,
        region_name=region_name
        or os.getenv("AWS_REGION")
        or os.getenv("AWS_DEFAULT_REGION"),
    )


def load_secret_request(
    secret_id: str,
    version_id: Optional[str] = None,
    version_stage: Optional[str] = None,
) -> SecretRequest:
    return SecretRequest(
        secret_id=secret_id, version_id=version_id, version_stage=version_stage
    )


def fetch_secret_value(secret_request: SecretRequest) -> SecretResponse:
    client = get_secret_client()
    kwargs: Dict[str, Any] = {"SecretId": secret_request.secret_id}
    if secret_request.version_id:
        kwargs["VersionId"] = secret_request.version_id
    if secret_request.version_stage:
        kwargs["VersionStage"] = secret_request.version_stage
    result = client.get_secret_value(**kwargs)
    payload = result.get("SecretString")
    if payload is None and result.get("SecretBinary") is not None:
        payload = result["SecretBinary"]
    return SecretResponse(
        secret_id=secret_request.secret_id,
        payload=normalize_secret_value(payload),
        version_id=result.get("VersionId"),
        version_stage=secret_request.version_stage,
    )
