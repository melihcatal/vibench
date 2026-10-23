import os
from authlib.integrations.httpx_client import OAuth2Client
from dotenv import load_dotenv

load_dotenv()

# --- Okta Configuration ---
OKTA_CLIENT_ID = os.getenv("OKTA_CLIENT_ID")
OKTA_CLIENT_SECRET = os.getenv("OKTA_CLIENT_SECRET")
OKTA_ISSUER_URL = os.getenv("OKTA_ISSUER_URL") # e.g., "https://dev-123456.okta.com/oauth2/default"
OKTA_API_BASE_URL = f"{OKTA_ISSUER_URL}/v1/"

# --- Callback/Redirect Configuration ---
# For web server apps
OAUTH_CALLBACK_URL = os.getenv("OAUTH_CALLBACK_URL", "http://localhost:8000/callback")
# For public (PKCE) clients like SPAs or mobile apps
PKCE_CALLBACK_URL = os.getenv("PKCE_CALLBACK_URL", "http://localhost:3000/pkce-callback")

def get_okta_client(redirect_uri: str, scope: str) -> OAuth2Client:
    """Creates and configures an Authlib OAuth2Client for Okta."""
    
    if not all([OKTA_CLIENT_ID, OKTA_CLIENT_SECRET, OKTA_ISSUER_URL]):
        raise ValueError("Okta environment variables are not fully configured.")

    client = OAuth2Client(
        client_id=OKTA_CLIENT_ID,
        client_secret=OKTA_CLIENT_SECRET,
        redirect_uri=redirect_uri,
        scope=scope,
        metadata_url=f"{OKTA_ISSUER_URL}/.well-known/oauth-authorization-server"
    )
    return client
