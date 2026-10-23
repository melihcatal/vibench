from authlib.integrations.requests_client import OAuth2Session
import os
from typing import Dict, Any

# Auth0 OAuth2 Provider Configuration
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN", "your-tenant.auth0.com")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID", "your-client-id")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET", "your-client-secret")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL", "http://localhost:5000/callback")
AUTH0_TOKEN_URL = f"https://{AUTH0_DOMAIN}/oauth/token"


def exchange_code_for_tokens(code: str, redirect_uri: str = None) -> Dict[str, Any]:
    """Exchange authorization code for tokens using Auth0 OAuth2 provider."""
    session = OAuth2Session(
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET,
        redirect_uri=redirect_uri or AUTH0_CALLBACK_URL,
    )
    token = session.fetch_token(
        url=AUTH0_TOKEN_URL,
        code=code,
        grant_type="authorization_code",
    )
    return token
