from authlib.integrations.requests_client import OAuth2Session
import os
from urllib.parse import urlencode

# Auth0 OAuth2 Provider Configuration
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "your-tenant.auth0.com")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "your-client-id")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "your-client-secret")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL", "http://localhost:5000/callback")
AUTH0_AUTHORIZATION_BASE_URL = f"https://{AUTH0_DOMAIN}/authorize"
AUTH0_TOKEN_URL = f"https://{AUTH0_DOMAIN}/oauth/token"
AUTH0_SCOPE = "openid profile email"


def start_oauth_login(state: str, redirect_uri: str = None) -> str:
    """Initiate OAuth2 authorization code flow with Auth0."""
    session = OAuth2Session(
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET,
        scope=AUTH0_SCOPE,
        redirect_uri=redirect_uri or AUTH0_CALLBACK_URL,
    )
    authorization_url, _ = session.create_authorization_url(
        AUTH0_AUTHORIZATION_BASE_URL,
        state=state,
        audience=f"https://{AUTH0_DOMAIN}/api/v2/",
    )
    return authorization_url
