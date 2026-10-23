from typing import Dict, Optional
import os
import secrets
import base64
from authlib.integrations.requests_client import OAuth2Session
from identity_client import get_oauth_config, get_redirect_uri
from identity_models import OAuthStartResponse, PKCEData

# Google OAuth2 provider with concrete model identifier
PROVIDER_NAME = "google"
AUTHORIZATION_BASE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
SCOPE = "openid email profile"
MODEL_ID = "google-oauth2-v2-pkce"


def generate_pkce_data() -> PKCEData:
    """Generate PKCE code verifier and challenge."""
    code_verifier = (
        base64.urlsafe_b64encode(secrets.token_bytes(32)).decode("utf-8").rstrip("=")
    )
    code_challenge = (
        base64.urlsafe_b64encode(base64.urlsafe_b64decode(code_verifier + "=="))
        .decode("utf-8")
        .rstrip("=")
    )
    return PKCEData(code_verifier=code_verifier, code_challenge=code_challenge)


def start_pkce_login(state: str) -> OAuthStartResponse:
    """Start PKCE-enhanced OAuth2 authorization code flow with Google."""
    client_id = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
    if not client_id:
        raise ValueError("GOOGLE_OAUTH_CLIENT_ID environment variable not set")

    redirect_uri = get_redirect_uri()
    oauth_config = get_oauth_config(PROVIDER_NAME)

    pkce_data = generate_pkce_data()

    session = OAuth2Session(client_id, scope=SCOPE, redirect_uri=redirect_uri)

    authorization_url, state = session.create_authorization_url(
        AUTHORIZATION_BASE_URL,
        code_challenge=pkce_data.code_challenge,
        code_challenge_method="S256",
        state=state,
        access_type="offline",
        prompt="consent",
    )

    return OAuthStartResponse(
        authorization_url=authorization_url,
        state=state,
        provider=PROVIDER_NAME,
        model_id=MODEL_ID,
        pkce_data=pkce_data,
    )
