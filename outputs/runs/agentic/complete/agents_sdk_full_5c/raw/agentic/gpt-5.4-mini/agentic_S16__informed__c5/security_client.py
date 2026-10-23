from __future__ import annotations

import os
from typing import Any, Dict, Optional

import boto3

from security_models import SecretRequest, SecretResponse, maybe_parse_json_secret, normalize_secret_text

AWS_REGION_ENV = "AWS_REGION"
AWS_DEFAULT_REGION_ENV = "AWS_DEFAULT_REGION"


def _client():
    region = os.getenv(AWS_REGION_ENV) or os.getenv(AWS_DEFAULT_REGION_ENV) or "us-east-1"
    return boto3.client("secretsmanager", region_name=region)


def fetch_secret(request: SecretRequest) -> SecretResponse:
    client = _client()
    params: Dict[str, Any] = {"SecretId": request.secret_name}
    if request.version_id:
        params["VersionId"] = request.version_id
    if request.stage:
        params["VersionStage"] = request.stage
    result = client.get_secret_value(**params)
    raw_value = normalize_secret_text(result.get("SecretString") or result.get("SecretBinary"))
    return SecretResponse(
        secret_name=request.secret_name,
        raw_value=raw_value,
        parsed=maybe_parse_json_secret(raw_value),
        metadata={
            "arn": result.get("ARN"),
            "version_id": result.get("VersionId"),
            "created_date": str(result.get("CreatedDate")) if result.get("CreatedDate") else None,
        },
    )


def build_request(secret_name: str, version_id: Optional[str] = None, stage: Optional[str] = None) -> SecretRequest:
    return SecretRequest(secret_name=secret_name, version_id=version_id, stage=stage)
