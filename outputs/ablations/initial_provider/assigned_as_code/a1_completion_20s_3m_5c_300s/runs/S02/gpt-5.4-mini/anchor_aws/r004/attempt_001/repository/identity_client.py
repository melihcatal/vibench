import os
from typing import Any, Dict

import requests


def load_identity_config() -> Dict[str, Any]:
    return {
        "domain_prefix": os.environ["COGNITO_DOMAIN_PREFIX"],
        "region": os.environ["AWS_REGION"],
        "client_id": os.environ["COGNITO_CLIENT_ID"],
        "client_secret": os.environ.get("COGNITO_CLIENT_SECRET"),
        "redirect_uri": os.environ.get("COGNITO_REDIRECT_URI"),
        "issuer": os.environ.get("COGNITO_ISSUER"),
    }


def cognito_token_endpoint(config: Dict[str, Any]) -> str:
    return f"https://{config['domain_prefix']}.auth.{config['region']}.amazoncognito.com/oauth2/token"


def exchange_code_for_tokens(code: str, redirect_uri: str, config: Dict[str, Any], code_verifier: str | None = None) -> Dict[str, Any]:
    data = {
        "grant_type": "authorization_code",
        "client_id": config["client_id"],
        "code": code,
        "redirect_uri": redirect_uri,
    }
    if code_verifier:
        data["code_verifier"] = code_verifier
    auth = None
    if config.get("client_secret"):
        auth = (config["client_id"], config["client_secret"])
    response = requests.post(cognito_token_endpoint(config), data=data, auth=auth, timeout=30)
    response.raise_for_status()
    return response.json()
