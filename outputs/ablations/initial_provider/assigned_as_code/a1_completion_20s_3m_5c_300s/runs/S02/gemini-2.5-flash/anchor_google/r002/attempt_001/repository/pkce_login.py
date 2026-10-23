import os
import base64
import hashlib
import requests
from urllib.parse import urlencode
from identity_client import get_oauth_config
from identity_models import TokenExchangeRequest, TokenExchangeResponse

def generate_pkce_codes():
    """Generates PKCE code_verifier and code_challenge."""
    code_verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).rstrip(b'=').decode('utf-8')
    return code_verifier, code_challenge

def get_auth0_authorize_url(config: dict, code_challenge: str) -> str:
    """Constructs the Auth0 authorization URL for PKCE flow."""
    params = {
        "audience": config["audience"],
        "scope": " ".join(config["scopes"]) if config["scopes"] else "openid profile email",
        "response_type": "code",
        "client_id": config["client_id"],
        "redirect_uri": config["redirect_uri"],
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }
    return f"https://{config['domain']}/authorize?{urlencode(params)}"

def exchange_auth0_code_for_tokens(token_exchange_request: TokenExchangeRequest, config: dict) -> TokenExchangeResponse:
    """Exchanges an authorization code for tokens with Auth0 using PKCE."""
    token_url = f"https://{config['domain']}/oauth/token"
    data = {
        "grant_type": "authorization_code",
        "client_id": config["client_id"],
        "code_verifier": token_exchange_request.code_verifier,
        "code": token_exchange_request.code,
        "redirect_uri": config["redirect_uri"],
    }

    response = requests.post(token_url, data=data, timeout=30)
    response.raise_for_status()
    token_data = response.json()

    return TokenExchangeResponse(
        access_token=token_data["access_token"],
        id_token=token_data["id_token"],
        token_type=token_data["token_type"],
        expires_in=token_data["expires_in"],
        refresh_token=token_data.get("refresh_token"),
    )

def pkce_login_start():
    """Starts the PKCE login flow by generating codes and returning the authorization URL."""
    code_verifier, code_challenge = generate_pkce_codes()
    config = get_oauth_config("auth0")
    authorization_url = get_auth0_authorize_url(config, code_challenge)
    return {"authorization_url": authorization_url, "code_verifier": code_verifier}

def pkce_login_callback(code: str, code_verifier: str) -> TokenExchangeResponse:
    """Handles the PKCE callback and exchanges the code for tokens."""
    config = get_oauth_config("auth0")
    token_request = TokenExchangeRequest(
        code=code,
        redirect_uri=config["redirect_uri"],
        client_id=config["client_id"],
        code_verifier=code_verifier,
    )
    token_response = exchange_auth0_code_for_tokens(token_request, config)
    return token_response
