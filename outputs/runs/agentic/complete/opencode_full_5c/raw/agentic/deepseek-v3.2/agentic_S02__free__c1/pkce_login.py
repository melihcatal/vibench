import os
import secrets
import hashlib
import base64
import urllib.parse
from authlib.integrations.requests_client import OAuth2Session
from identity_client import get_oauth_client_config


def generate_pkce_verifier():
    """Generate a secure PKCE code verifier."""
    return secrets.token_urlsafe(64)


def generate_pkce_challenge(code_verifier):
    """Generate PKCE code challenge from verifier using S256 method."""
    code_challenge = hashlib.sha256(code_verifier.encode()).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode().rstrip("=")
    return code_challenge


def start_pkce_authorization(provider="google", scopes=None):
    """Start PKCE authorization flow for public clients."""
    config = get_oauth_client_config(provider)

    client_id = config["client_id"]
    redirect_uri = config["redirect_uri"]
    authorization_endpoint = config["authorization_endpoint"]

    if scopes is None:
        scopes = config.get("scope", "openid email profile").split()

    if provider == "github":
        scopes = ["user:email"] + scopes

    state = secrets.token_urlsafe(16)
    code_verifier = generate_pkce_verifier()
    code_challenge = generate_pkce_challenge(code_verifier)

    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": " ".join(scopes),
        "state": state,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }

    if provider == "google":
        params["access_type"] = "offline"
        params["prompt"] = "consent"

    query_string = urllib.parse.urlencode(params)
    authorization_url = f"{authorization_endpoint}?{query_string}"

    return {
        "authorization_url": authorization_url,
        "state": state,
        "code_verifier": code_verifier,
        "provider": provider,
    }


def exchange_pkce_code(
    authorization_code, code_verifier, state, received_state, provider="google"
):
    """Exchange PKCE authorization code for tokens."""
    if state != received_state:
        raise ValueError("State mismatch - possible CSRF attack")

    config = get_oauth_client_config(provider)

    client_id = config["client_id"]
    redirect_uri = config["redirect_uri"]
    token_endpoint = config["token_endpoint"]

    session = OAuth2Session(client_id, redirect_uri=redirect_uri)

    token_response = session.fetch_token(
        token_endpoint,
        grant_type="authorization_code",
        code=authorization_code,
        redirect_uri=redirect_uri,
        code_verifier=code_verifier,
    )

    return {
        "access_token": token_response["access_token"],
        "token_type": token_response.get("token_type", "Bearer"),
        "expires_in": token_response.get("expires_in", 3600),
        "refresh_token": token_response.get("refresh_token"),
        "id_token": token_response.get("id_token"),
        "provider": provider,
    }


def validate_pkce_flow(provider="google"):
    """Validate that provider supports PKCE."""
    config = get_oauth_client_config(provider)

    if not config.get("supports_pkce", True):
        raise ValueError(f"Provider {provider} does not support PKCE")

    required_params = [
        "client_id",
        "redirect_uri",
        "authorization_endpoint",
        "token_endpoint",
    ]
    for param in required_params:
        if param not in config:
            raise ValueError(f"Missing required configuration: {param}")

    return True


def get_pkce_supported_providers():
    """Get list of providers that support PKCE."""
    return ["google", "microsoft", "github", "okta", "auth0"]
