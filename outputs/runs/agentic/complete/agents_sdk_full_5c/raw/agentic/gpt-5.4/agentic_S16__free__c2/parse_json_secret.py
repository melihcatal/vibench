from __future__ import annotations

from typing import Any, Dict

from security_client import build_secret_name, get_secrets_manager_client
from security_models import parse_json_secret_string


JSON_SECRET_NAME = build_secret_name("services/payment_gateway")


def parse_json_secret(secret_id: str = JSON_SECRET_NAME) -> Dict[str, Any]:
    client = get_secrets_manager_client()
    response = client.get_secret_value(SecretId=secret_id, VersionStage="AWSCURRENT")
    secret_obj = parse_json_secret_string(response["SecretString"])
    secret_obj["_provider"] = "aws-secrets-manager"
    secret_obj["_version_id"] = response.get("VersionId")
    return secret_obj
