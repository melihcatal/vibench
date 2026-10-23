from authlib.integrations.requests_client import OAuth2Session
import os
import secrets
import base64
import hashlib

# Auth0 OAuth2 Provider Configuration
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "your-tenant.auth0.com")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "your-client-id")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL", "http://localhost:5000/callback")
AUTH0_AUTHORIZATION_BASE_URL = f"https://{AUTH0_DOMAIN}/authorize"
AUTH0_TOKEN_URL = f"https://{AUTH0_DOMAIN}/oauth/token"
AUTH0_SCOPE = "openid profile email"


def generate_pkce_codes() -> tuple:
    """Generate PKCE code verifier and challenge."""
    code_verifier = secrets.token_urlsafe(64)
    code_challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode()).digest())
        .decode()
        .rstrip("=")
    )
    return code_verifier, code_challenge


def start_pkce_login(state: str, redirect_uri: str = None) -> tuple:
    """Initiate PKCE-enhanced OAuth2 authorization code flow with Auth0."""
    code_verifier, code_challenge = generate_pkce_codes()
    session = OAuth2Session(
        client_id=AUTH0_CLIENT_ID,
        scope=AUTH0_SCOPE,
        redirect_uri=redirect_uri or AUTH0_CALLBACK_URL,
    )
    authorization_url, _ = session.create_authorization_url(
        AUTH0_AUTHORIZATION_BASE_URL,
        state=state,
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )
    return authorization_url, code_verifier
