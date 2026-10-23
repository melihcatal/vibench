import os
from dataclasses import asdict
from typing import Any, Dict, Optional

import boto3

from security_models import SecretRequest, SecretResponse, normalize_secret_value


def build_secrets_manager_client(region_name: Optional[str] = None):
    return boto3.client(
        "secretsmanager", region_name=region_name or os.environ.get("AWS_REGION")
    )


def secret_request(
    name: str, version: Optional[str] = None, stage: Optional[str] = None
) -> SecretRequest:
    return SecretRequest(name=name, version=version, stage=stage)


def fetch_secret_payload(request: SecretRequest, client: Any = None) -> SecretResponse:
    sm = client or build_secrets_manager_client()
    kwargs: Dict[str, Any] = {"SecretId": request.name}
    if request.version:
        kwargs["VersionId"] = request.version
    if request.stage:
        kwargs["VersionStage"] = request.stage
    result = sm.get_secret_value(**kwargs)
    value = result.get("SecretString") or result.get("SecretBinary")
    return SecretResponse(
        name=request.name,
        value=normalize_secret_value(value),
        version=result.get("VersionId"),
        metadata={
            k: v for k, v in result.items() if k not in {"SecretString", "SecretBinary"}
        },
    )


def to_dict(response: SecretResponse) -> Dict[str, Any]:
    return asdict(response)
