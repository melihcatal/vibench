import os
import requests
from typing import Dict, Any
from .identity_models import AuthConfig, Tokens


def get_auth_config() -> AuthConfig:
    return AuthConfig(
        domain=os.getenv("COGNITO_DOMAIN"),
        client_id=os.getenv("COGNITO_CLIENT_ID"),
        client_secret=os.getenv("COGNITO_CLIENT_SECRET", ""),
        redirect_uri=os.getenv("REDIRECT_URI", "http://localhost:8080/callback"),
    )


def exchange_authorization_code(
    config: AuthConfig, code: str, code_verifier: str = None
) -> Tokens:
    token_url = f"https://{config.domain}/oauth2/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": config.client_id,
        "redirect_uri": config.redirect_uri,
        "code": code,
    }
    if code_verifier:
        data["code_verifier"] = code_verifier
    else:
        if not config.client_secret:
            raise ValueError("Client secret required for non-PKCE flow")
        data["client_secret"] = config.client_secret
    response = requests.post(token_url, data=data)
    response.raise_for_status()
    tokens_dict = response.json()
    return Tokens(
        access_token=tokens_dict["access_token"],
        id_token=tokens_dict["id_token"],
        refresh_token=tokens_dict.get("refresh_token", ""),
        token_type=tokens_dict.get("token_type", "Bearer"),
        expires_in=tokens_dict.get("expires_in", 3600),
    )


def fetch_user_profile(config: AuthConfig, tokens: Tokens) -> Dict[str, Any]:
    userinfo_url = f"https://{config.domain}/oauth2/userInfo"
    headers = {"Authorization": f"{tokens.token_type} {tokens.access_token}"}
    response = requests.get(userinfo_url, headers=headers)
    response.raise_for_status()
    return response.json()
