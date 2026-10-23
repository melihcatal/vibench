import secrets
import hashlib
import base64
from urllib.parse import urlencode
from identity_client import get_cognito_config

def generate_pkce_challenge():
    code_verifier = secrets.token_urlsafe(96)  # Generate a 128-byte verifier, URL-safe base64 encoded
    s256 = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(s256).decode('utf-8').replace('=', '')
    return code_verifier, code_challenge

def start_pkce_login(redirect_uri: str, config=None) -> dict:
    config = config or get_cognito_config()
    state = secrets.token_urlsafe(32)
    code_verifier, code_challenge = generate_pkce_challenge()

    domain = f"https://{config.domain_prefix}.auth.{config.region}.amazoncognito.com"
    query = {"response_type": "code", "client_id": config.client_id,
             "redirect_uri": redirect_uri, "scope": "openid email profile", "state": state,
             "code_challenge": code_challenge, "code_challenge_method": "S256"}
    if getattr(config, "identity_provider", None):
        query["identity_provider"] = config.identity_provider
    return {"authorization_url": domain + "/oauth2/authorize?" + urlencode(query), "session_id": state, "code_verifier": code_verifier}

def exchange_pkce_code_for_tokens(code: str, redirect_uri: str, code_verifier: str) -> dict:
    config = get_cognito_config()
    token_endpoint = config.token_endpoint
    client_id = config.client_id

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "code": code,
        "redirect_uri": redirect_uri,
        "code_verifier": code_verifier,
    }

    if config.client_secret:
        data["client_secret"] = config.client_secret

    try:
        response = requests.post(token_endpoint, headers=headers, data=urlencode(data))
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as e:
        raise RuntimeError(f"Failed to exchange PKCE code for tokens: {e}. Response: {e.response.text}")
    except Exception as e:
        raise RuntimeError(f"An error occurred during PKCE token exchange: {e}")
