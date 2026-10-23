import os
from typing import Any, Dict, Optional

import boto3

from identity_models import compact_text, normalize_email


def config_value(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.environ.get(name, default)
    return value.strip() if isinstance(value, str) else value


def cognito_client():
    region = config_value("AWS_REGION", config_value("AWS_DEFAULT_REGION", "us-east-1"))
    return boto3.client("cognito-idp", region_name=region)


def user_pool_id() -> str:
    return config_value("COGNITO_USER_POOL_ID", "") or ""


def app_client_id() -> str:
    return config_value("COGNITO_APP_CLIENT_ID", "") or ""


def normalize_username(email: str) -> str:
    return normalize_email(email)


def normalize_name(value: Optional[str]) -> str:
    return compact_text(value)


def auth_params(email: str, password: str) -> Dict[str, str]:
    return {"USERNAME": normalize_username(email), "PASSWORD": password}


def refresh_params(refresh_token: str) -> Dict[str, str]:
    return {"REFRESH_TOKEN": refresh_token}


def secret_hash_identity(
    client_id: str, username: str, client_secret: Optional[str]
) -> Optional[str]:
    if not client_secret:
        return None
    import base64
    import hashlib
    import hmac

    mac = hmac.new(
        client_secret.encode(), (username + client_id).encode(), hashlib.sha256
    )
    return base64.b64encode(mac.digest()).decode()
