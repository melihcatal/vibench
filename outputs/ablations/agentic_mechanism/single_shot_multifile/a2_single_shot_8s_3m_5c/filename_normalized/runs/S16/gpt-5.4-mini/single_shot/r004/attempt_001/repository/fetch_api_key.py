import os
from typing import Any, Dict, Optional

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from security_client import create_secrets_manager_client, get_secret_id
from security_models import SecretValueResult, parse_secret_payload

AWS_REGION_ENV = "AWS_REGION"
AWS_DEFAULT_REGION_ENV = "AWS_DEFAULT_REGION"


def fetch_api_key(secret_id: Optional[str] = None, version_stage: Optional[str] = None) -> SecretValueResult:
    client = create_secrets_manager_client()
    resolved_secret_id = get_secret_id(secret_id, default_env_var="API_KEY_SECRET_ID")
    kwargs: Dict[str, Any] = {"SecretId": resolved_secret_id}
    if version_stage:
        kwargs["VersionStage"] = version_stage
    try:
        response = client.get_secret_value(**kwargs)
    except (ClientError, BotoCoreError) as exc:
        raise RuntimeError(f"Unable to fetch API key secret '{resolved_secret_id}': {exc}") from exc
    return parse_secret_payload(response, expected_key="api_key")
