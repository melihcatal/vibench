from authlib.integrations.requests_client import OAuth2Session
import os
import secrets
import base64
import hashlib

# Okta OAuth2 Provider Configuration for PKCE
OKTA_DOMAIN = os.getenv("OKTA_DOMAIN", "your-org.okta.com")
OKTA_CLIENT_ID = os.getenv("OKTA_CLIENT_ID", "your-client-id")
OKTA_CALLBACK_URL = os.getenv("OKTA_CALLBACK_URL", "http://localhost:5000/callback")
OKTA_AUTHORIZATION_BASE_URL = f"https://{OKTA_DOMAIN}/oauth2/default/v1/authorize"
OKTA_TOKEN_URL = f"https://{OKTA_DOMAIN}/oauth2/default/v1/token"
OKTA_SCOPE = "openid profile email"


def generate_pkce_codes() -> tuple:
    """Generate PKCE code verifier and challenge for Okta OAuth2 provider."""
    code_verifier = secrets.token_urlsafe(64)
    code_challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest())
        .decode()
        .rstrip("=")
    )
    return code_verifier, code_challenge


def start_pkce_login(state: str) -> tuple:
    """Initiate PKCE OAuth2 flow with Okta."""
    code_verifier, code_challenge = generate_pkce_codes()
    session = OAuth2Session(
        client_id=OKTA_CLIENT_ID,
        scope=OKTA_SCOPE,
        redirect_uri=OKTA_CALLBACK_URL,
    )
    authorization_url, _ = session.create_authorization_url(
        OKTA_AUTHORIZATION_BASE_URL,
        code_challenge=code_challenge,
        code_challenge_method="S256",
        state=state,
    )
    return authorization_url, code_verifier
