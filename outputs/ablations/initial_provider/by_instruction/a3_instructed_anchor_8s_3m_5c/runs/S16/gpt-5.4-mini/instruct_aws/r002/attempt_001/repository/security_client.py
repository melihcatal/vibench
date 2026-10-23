import json
import os
from typing import Any, Dict, Optional

import boto3

from security_models import SecretRequest, SecretResponse, normalize_secret_payload


def build_secrets_manager_client(region_name: Optional[str] = None):
    return boto3.client("secretsmanager", region_name=region_name or os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION"))


def load_secret(request: SecretRequest, region_name: Optional[str] = None) -> SecretResponse:
    client = build_secrets_manager_client(region_name)
    kwargs: Dict[str, Any] = {"SecretId": request.secret_id}
    if request.version_stage:
        kwargs["VersionStage"] = request.version_stage
    if request.version_id:
        kwargs["VersionId"] = request.version_id
    response = client.get_secret_value(**kwargs)
    secret_string = response.get("SecretString")
    if secret_string is not None:
        try:
            payload = json.loads(secret_string)
        except json.JSONDecodeError:
            payload = {"secret_string": secret_string}
    else:
        payload = {"secret_binary": response.get("SecretBinary")}
    return SecretResponse(
        secret_id=request.secret_id,
        payload=normalize_secret_payload(payload),
        version_stage=response.get("VersionStages", [None])[0],
        version_id=response.get("VersionId"),
    )


def secret_value_field(secret: SecretResponse, field_name: str, default: Any = None) -> Any:
    return secret.payload.get(field_name, default)
