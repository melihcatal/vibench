import base64
import hashlib
import os
import secrets
from typing import Dict, Optional

import boto3
from botocore.config import Config

from identity_models import OAuthLoginRequest


def get_cognito_config() -> Dict[str, str]:
    return {
        "region": os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1")),
        "user_pool_domain": os.environ.get("COGNITO_DOMAIN", ""),
        "client_id": os.environ.get("COGNITO_CLIENT_ID", ""),
        "redirect_uri": os.environ.get("COGNITO_REDIRECT_URI", ""),
        "user_pool_id": os.environ.get("COGNITO_USER_POOL_ID", ""),
        "app_client_secret": os.environ.get("COGNITO_CLIENT_SECRET", ""),
    }


def cognito_client():
    cfg = get_cognito_config()
    return boto3.client("cognito-idp", region_name=cfg["region"], config=Config(retries={"max_attempts": 3}))


def build_authorize_url(login: OAuthLoginRequest) -> str:
    cfg = get_cognito_config()
    base = f"https://{cfg['user_pool_domain']}.auth.{cfg['region']}.amazoncognito.com/oauth2/authorize"
    params = [
        ("response_type", "code"),
        ("client_id", login.client_id),
        ("redirect_uri", login.redirect_uri),
        ("scope", login.scope),
    ]
    if login.state:
        params.append(("state", login.state))
    if login.code_challenge:
        params.append(("code_challenge", login.code_challenge))
    if login.code_challenge_method:
        params.append(("code_challenge_method", login.code_challenge_method))
    query = "&".join(f"{k}={_urlencode(v)}" for k, v in params)
    return f"{base}?{query}"


def exchange_code_for_tokens(code: str, redirect_uri: str, code_verifier: Optional[str] = None) -> Dict[str, object]:
    cfg = get_cognito_config()
    token_url = f"https://{cfg['user_pool_domain']}.auth.{cfg['region']}.amazoncognito.com/oauth2/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": cfg["client_id"],
        "code": code,
        "redirect_uri": redirect_uri,
    }
    if code_verifier:
        data["code_verifier"] = code_verifier
    import requests
    resp = requests.post(token_url, data=data, timeout=20)
    resp.raise_for_status()
    return resp.json()


def generate_pkce_pair() -> Dict[str, str]:
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b"=").decode("ascii")
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode("ascii")).digest()).rstrip(b"=").decode("ascii")
    return {"code_verifier": verifier, "code_challenge": challenge}


def _urlencode(value: str) -> str:
    from urllib.parse import quote
    return quote(value, safe="")
