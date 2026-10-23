import os
import secrets
import urllib.parse
from authlib.integrations.requests_client import OAuth2Session
from identity_client import get_oauth_client_config


def start_oauth_login(provider="google"):
    """Start OAuth/OpenID Connect authorization code flow."""
    config = get_oauth_client_config(provider)

    client_id = config["client_id"]
    redirect_uri = config["redirect_uri"]
    authorization_endpoint = config["authorization_endpoint"]
    scope = config.get("scope", "openid email profile")

    state = secrets.token_urlsafe(16)
    nonce = secrets.token_urlsafe(16) if config.get("use_nonce", True) else None

    session = OAuth2Session(client_id, redirect_uri=redirect_uri, scope=scope)

    authorization_url, _ = session.create_authorization_url(
        authorization_endpoint, state=state, nonce=nonce
    )

    if provider == "google":
        authorization_url += "&access_type=offline&prompt=consent"

    return {
        "authorization_url": authorization_url,
        "state": state,
        "nonce": nonce,
        "provider": provider,
    }


def start_pkce_login(provider="google"):
    """Start PKCE-enhanced OAuth flow for public clients."""
    config = get_oauth_client_config(provider)

    client_id = config["client_id"]
    redirect_uri = config["redirect_uri"]
    authorization_endpoint = config["authorization_endpoint"]
    scope = config.get("scope", "openid email profile")

    state = secrets.token_urlsafe(16)
    code_verifier = secrets.token_urlsafe(64)

    from authlib.oauth2.rfc7636 import create_s256_code_challenge

    code_challenge = create_s256_code_challenge(code_verifier)

    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
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
