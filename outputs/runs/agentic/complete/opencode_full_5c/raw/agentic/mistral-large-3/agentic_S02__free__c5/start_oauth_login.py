from typing import Dict, Optional
import os
import requests
from authlib.integrations.requests_client import OAuth2Session
from identity_client import get_oauth_config, get_redirect_uri
from identity_models import OAuthStartResponse

# Google OAuth2 provider with concrete model identifier
PROVIDER_NAME = "google"
AUTHORIZATION_BASE_URL = "https://accounts.google.com/o/oauth2/v2/auth"
SCOPE = "openid email profile"
MODEL_ID = "google-oauth2-v2"


def start_oauth_login(
    state: str, code_verifier: Optional[str] = None
) -> OAuthStartResponse:
    """Start OAuth2 authorization code flow with Google as the provider."""
    client_id = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
    if not client_id:
        raise ValueError("GOOGLE_OAUTH_CLIENT_ID environment variable not set")

    redirect_uri = get_redirect_uri()
    oauth_config = get_oauth_config(PROVIDER_NAME)

    session = OAuth2Session(client_id, scope=SCOPE, redirect_uri=redirect_uri)

    if code_verifier:
        authorization_url, state = session.create_authorization_url(
            AUTHORIZATION_BASE_URL,
            code_verifier=code_verifier,
            state=state,
            access_type="offline",
            prompt="consent",
        )
    else:
        authorization_url, state = session.create_authorization_url(
            AUTHORIZATION_BASE_URL, state=state, access_type="offline", prompt="consent"
        )

    return OAuthStartResponse(
        authorization_url=authorization_url,
        state=state,
        provider=PROVIDER_NAME,
        model_id=MODEL_ID,
    )
