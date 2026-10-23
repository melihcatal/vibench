from typing import Dict
import os
import requests
from authlib.integrations.requests_client import OAuth2Session
from identity_client import get_oauth_config, get_redirect_uri
from identity_models import TokenResponse

# Google OAuth2 provider with concrete model identifier
PROVIDER_NAME = "google"
TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"
MODEL_ID = "google-oauth2-v2"


def handle_oauth_callback(
    code: str, state: str, code_verifier: str = None
) -> TokenResponse:
    """Exchange authorization code for tokens using Google's OAuth2 API."""
    client_id = os.getenv("GOOGLE_OAUTH_CLIENT_ID")
    client_secret = os.getenv("GOOGLE_OAUTH_CLIENT_SECRET")
    if not client_id or not client_secret:
        raise ValueError("Google OAuth credentials not set in environment variables")

    redirect_uri = get_redirect_uri()
    oauth_config = get_oauth_config(PROVIDER_NAME)

    session = OAuth2Session(
        client_id, client_secret=client_secret, redirect_uri=redirect_uri
    )

    token_data = session.fetch_token(
        TOKEN_ENDPOINT, code=code, code_verifier=code_verifier
    )

    return TokenResponse(
        access_token=token_data.get("access_token"),
        refresh_token=token_data.get("refresh_token"),
        id_token=token_data.get("id_token"),
        expires_in=token_data.get("expires_in"),
        token_type=token_data.get("token_type"),
        provider=PROVIDER_NAME,
        model_id=MODEL_ID,
    )
