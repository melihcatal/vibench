from __future__ import annotations

import json
import os
from dataclasses import asdict
from typing import Any, Dict, Optional

import boto3
from boto3.session import Session

from security_models import NormalizedLabel, SecretRequest, SecretResponse, normalize_secret_value

AWS_REGION_ENV = "AWS_REGION"
AWS_DEFAULT_REGION_ENV = "AWS_DEFAULT_REGION"


def get_aws_region(explicit_region: Optional[str] = None) -> str:
    if explicit_region:
        return explicit_region
    return os.getenv(AWS_REGION_ENV) or os.getenv(AWS_DEFAULT_REGION_ENV) or "us-east-1"


def build_secretsmanager_client(region_name: Optional[str] = None):
    session: Session = boto3.session.Session(region_name=get_aws_region(region_name))
    return session.client("secretsmanager")


def get_secret_value(request: SecretRequest) -> SecretResponse:
    client = build_secretsmanager_client(request.region)
    params: Dict[str, Any] = {"SecretId": request.secret_name}
    if request.version_id:
        params["VersionId"] = request.version_id
    if request.version_stage:
        params["VersionStage"] = request.version_stage
    response = client.get_secret_value(**params)
    value = response.get("SecretString")
    if value is None and response.get("SecretBinary") is not None:
        value = response["SecretBinary"]
    return SecretResponse(
        secret_name=request.secret_name,
        value=normalize_secret_value(value),
        version_id=response.get("VersionId"),
        version_stage=request.version_stage,
        metadata={k: v for k, v in response.items() if k not in {"SecretString", "SecretBinary"}},
    )


def parse_json_payload(payload: str) -> Dict[str, Any]:
    return json.loads(payload or "{}")


def label_safety_summary(label: str) -> NormalizedLabel:
    forbidden = ("password", "secret", "token", "apikey", "api key")
    normalized = label.strip()
    issues = tuple(term for term in forbidden if term in normalized.lower())
    return NormalizedLabel(label=normalized, safe=not issues, issues=issues)


def response_as_dict(response: SecretResponse) -> Dict[str, Any]:
    return asdict(response)
