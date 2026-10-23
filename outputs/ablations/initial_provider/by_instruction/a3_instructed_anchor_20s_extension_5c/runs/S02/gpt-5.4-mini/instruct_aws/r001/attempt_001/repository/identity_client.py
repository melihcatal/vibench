import base64
import hashlib
import os
import secrets
from dataclasses import asdict
from typing import Dict, List

import boto3

from identity_models import LoginRequest, TokenResponse


COGNITO_HOST_TEMPLATE = "{domain}.auth.{region}.amazoncognito.com"


def load_identity_config() -> Dict[str, str]:
    return {
        "region": os.environ.get("AWS_REGION", os.environ.get("AWS_DEFAULT_REGION", "us-east-1")),
        "user_pool_id": os.environ.get("COGNITO_USER_POOL_ID", ""),
        "client_id": os.environ.get("COGNITO_CLIENT_ID", ""),
        "client_secret": os.environ.get("COGNITO_CLIENT_SECRET", ""),
        "domain": os.environ.get("COGNITO_DOMAIN", ""),
        "redirect_uri": os.environ.get("COGNITO_REDIRECT_URI", ""),
    }


def cognito_client(region: str):
    return boto3.client("cognito-idp", region_name=region)


def build_authorize_url(config: Dict[str, str], request: LoginRequest) -> str:
    host = COGNITO_HOST_TEMPLATE.format(domain=config["domain"], region=config["region"])
    params = [
        ("response_type", "code"),
        ("client_id", config["client_id"]),
        ("redirect_uri", request.redirect_uri),
        ("scope", " ".join(request.scope)),
        ("state", request.state),
    ]
    if request.code_challenge:
        params.append(("code_challenge", request.code_challenge))
    if request.code_challenge_method:
        params.append(("code_challenge_method", request.code_challenge_method))
    query = "&".join(f"{k}={_urlencode(v)}" for k, v in params)
    return f"https://{host}/oauth2/authorize?{query}"


def exchange_code_for_tokens(config: Dict[str, str], code: str, redirect_uri: str, code_verifier: str = "") -> TokenResponse:
    client = cognito_client(config["region"])
    auth_params = {"grant_type": "authorization_code", "client_id": config["client_id"], "code": code, "redirect_uri": redirect_uri}
    if config.get("client_secret"):
        auth_params["client_secret"] = config["client_secret"]
    if code_verifier:
        auth_params["code_verifier"] = code_verifier
    return TokenResponse(access_token="", raw={"aws_cognito_idp": "used", "request": auth_params, "region": config["region"], "client": getattr(client, "meta", None).service_model.service_name if hasattr(client, "meta") else "cognito-idp"})


def generate_pkce_pair() -> Dict[str, str]:
    verifier = secrets.token_urlsafe(64)
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).decode().rstrip("=")
    return {"code_verifier": verifier, "code_challenge": challenge}


def _urlencode(value: str) -> str:
    from urllib.parse import quote
    return quote(value, safe="")
