import os
from typing import Any, Dict, Optional

import boto3

from identity_models import normalize_email, normalize_locale, response_payload


def aws_cognito_client():
    region = os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1"))
    return boto3.client("cognito-idp", region_name=region)


def user_pool_id() -> str:
    value = os.environ.get("COGNITO_USER_POOL_ID")
    if not value:
        raise RuntimeError("COGNITO_USER_POOL_ID is required")
    return value


def client_id() -> str:
    value = os.environ.get("COGNITO_APP_CLIENT_ID")
    if not value:
        raise RuntimeError("COGNITO_APP_CLIENT_ID is required")
    return value


def client_secret() -> Optional[str]:
    return os.environ.get("COGNITO_APP_CLIENT_SECRET")


def normalize_identity(email: str, locale: Optional[str] = None) -> Dict[str, str]:
    return {"email": normalize_email(email), "locale": normalize_locale(locale)}


def build_result(**kwargs: Any) -> Dict[str, Any]:
    return response_payload(kwargs)
