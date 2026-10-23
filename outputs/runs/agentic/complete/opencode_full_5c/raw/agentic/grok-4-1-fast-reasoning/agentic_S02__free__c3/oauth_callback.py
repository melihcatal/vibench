import requests
from typing import Optional
from .identity_client import get_google_confidential_config
from .identity_models import OAuthConfig, TokenResponse


def exchange_authorization_code(
    code: str, config: Optional[OAuthConfig] = None, code_verifier: Optional[str] = None
) -> TokenResponse:
    if config is None:
        config = get_google_confidential_config()
    data = {
        "client_id": config.client_id,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": config.redirect_uri,
    }
    if config.client_secret:
        data["client_secret"] = config.client_secret
    if code_verifier:
        data["code_verifier"] = code_verifier
    response = requests.post(config.token_url, data=data)
    response.raise_for_status()
    tokens = response.json()
    return TokenResponse(**tokens)
