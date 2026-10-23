import os
import secrets
from dataclasses import asdict
from typing import Dict

from identity_models import OAuthLoginRequest


def load_identity_config() -> Dict[str, str]:
    return {
        "aws_region": os.getenv("AWS_REGION", "us-east-1"),
        "cognito_domain": os.getenv("COGNITO_DOMAIN", ""),
        "cognito_user_pool_client_id": os.getenv("COGNITO_USER_POOL_CLIENT_ID", ""),
        "cognito_user_pool_client_secret": os.getenv("COGNITO_USER_POOL_CLIENT_SECRET", ""),
        "redirect_uri": os.getenv("OAUTH_REDIRECT_URI", "https://example.com/oauth/callback"),
        "scope": os.getenv("OAUTH_SCOPE", "openid profile email"),
    }


def build_login_request() -> OAuthLoginRequest:
    cfg = load_identity_config()
    return OAuthLoginRequest(
        client_id=cfg["cognito_user_pool_client_id"],
        redirect_uri=cfg["redirect_uri"],
        scope=cfg["scope"],
        state=secrets.token_urlsafe(24),
    )


def login_request_to_dict(request: OAuthLoginRequest) -> Dict[str, str]:
    data = asdict(request)
    return {k: v for k, v in data.items() if v is not None}
