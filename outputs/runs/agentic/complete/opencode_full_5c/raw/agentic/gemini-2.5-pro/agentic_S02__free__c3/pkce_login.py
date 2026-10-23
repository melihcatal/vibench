import requests
from urllib.parse import urlencode
from identity_client import get_auth0_config, generate_pkce_params


def start_auth0_pkce_login():
    """
    Starts an OAuth 2.0 authorization code flow with PKCE for Auth0.
    """
    config = get_auth0_config()
    pkce_params = generate_pkce_params()

    params = {
        "client_id": config.client_id,
        "response_type": "code",
        "scope": config.scope,
        "redirect_uri": config.redirect_uri,
        "code_challenge": pkce_params.code_challenge,
        "code_challenge_method": pkce_params.code_challenge_method,
        "audience": f"https://{config.client_id.split('@')[0]}.us.auth0.com/api/v2/",  # Example audience
    }

    authorization_url = f"{config.authorization_endpoint}?{urlencode(params)}"
    return authorization_url, pkce_params.code_verifier


def exchange_pkce_code_for_token(authorization_code: str, code_verifier: str):
    """
    Exchanges the authorization code for a token using PKCE.
    """
    config = get_auth0_config()

    payload = {
        "grant_type": "authorization_code",
        "client_id": config.client_id,
        "code": authorization_code,
        "redirect_uri": config.redirect_uri,
        "code_verifier": code_verifier,
    }

    response = requests.post(config.token_endpoint, data=payload)
    response.raise_for_status()
    return response.json()
