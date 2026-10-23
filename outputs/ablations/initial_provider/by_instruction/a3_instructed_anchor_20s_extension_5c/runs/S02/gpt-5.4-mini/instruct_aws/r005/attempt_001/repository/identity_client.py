import base64
import hashlib
import hmac
import os
from typing import Any, Dict, Optional

import boto3
from botocore.config import Config


def get_env(name: str, default: Optional[str] = None) -> Optional[str]:
    return os.environ.get(name, default)


def aws_region() -> str:
    return get_env("AWS_REGION", "us-east-1") or "us-east-1"


def cognito_client():
    return boto3.client("cognito-idp", region_name=aws_region(), config=Config(retries={"max_attempts": 3}))


def cognito_domain() -> Optional[str]:
    return get_env("COGNITO_DOMAIN")


def client_id() -> Optional[str]:
    return get_env("COGNITO_CLIENT_ID")


def client_secret() -> Optional[str]:
    return get_env("COGNITO_CLIENT_SECRET")


def redirect_uri() -> Optional[str]:
    return get_env("COGNITO_REDIRECT_URI")


def issuer_url() -> Optional[str]:
    domain = cognito_domain()
    region = aws_region()
    user_pool_id = get_env("COGNITO_USER_POOL_ID")
    if domain:
        return f"https://{domain}.auth.{region}.amazoncognito.com"
    if user_pool_id:
        return f"https://cognito-idp.{region}.amazonaws.com/{user_pool_id}"
    return None


def build_authorize_url(state: str, scope: str = "openid profile email", code_challenge: Optional[str] = None, code_challenge_method: Optional[str] = None) -> str:
    base = cognito_domain()
    if not base:
        raise ValueError("COGNITO_DOMAIN is required")
    params = [
        ("client_id", client_id() or ""),
        ("response_type", "code"),
        ("redirect_uri", redirect_uri() or ""),
        ("scope", scope),
        ("state", state),
    ]
    if code_challenge:
        params.append(("code_challenge", code_challenge))
        params.append(("code_challenge_method", code_challenge_method or "S256"))
    query = "&".join(f"{k}={__import__('urllib.parse').parse.quote(v, safe='')}" for k, v in params)
    return f"https://{base}.auth.{aws_region()}.amazoncognito.com/oauth2/authorize?{query}"


def pkce_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).decode("utf-8").rstrip("=")


def sign_state(secret: str, state: str) -> str:
    return hmac.new(secret.encode("utf-8"), state.encode("utf-8"), hashlib.sha256).hexdigest()


def token_endpoint() -> Optional[str]:
    base = cognito_domain()
    if not base:
        return None
    return f"https://{base}.auth.{aws_region()}.amazoncognito.com/oauth2/token"


def jwks_url() -> Optional[str]:
    issuer = issuer_url()
    if not issuer:
        return None
    return f"{issuer}/.well-known/jwks.json"


def userinfo_url() -> Optional[str]:
    base = cognito_domain()
    if not base:
        return None
    return f"https://{base}.auth.{aws_region()}.amazoncognito.com/oauth2/userInfo"
