import os
from authlib.integrations.httpx_client import OAuth2Client

# --- Okta Configuration ---
OKTA_DOMAIN = os.environ.get("OKTA_DOMAIN")
OKTA_CLIENT_ID = os.environ.get("OKTA_CLIENT_ID")
OKTA_CLIENT_SECRET = os.environ.get("OKTA_CLIENT_SECRET")

okta_client = None
if OKTA_DOMAIN and OKTA_CLIENT_ID and OKTA_CLIENT_SECRET:
    okta_client = OAuth2Client(
        client_id=OKTA_CLIENT_ID,
        client_secret=OKTA_CLIENT_SECRET,
        scope="openid profile email",
        redirect_uri="http://localhost:8000/callback/okta",
        metadata_url=f"https://{OKTA_DOMAIN}/.well-known/openid-configuration",
    )

# --- Auth0 Configuration for PKCE ---
AUTH0_DOMAIN = os.environ.get("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.environ.get("AUTH0_CLIENT_ID")

auth0_pkce_client = None
if AUTH0_DOMAIN and AUTH0_CLIENT_ID:
    auth0_pkce_client = OAuth2Client(
        client_id=AUTH0_CLIENT_ID,
        scope="openid profile email",
        redirect_uri="http://localhost:8000/callback/auth0",
        metadata_url=f"https://{AUTH0_DOMAIN}/.well-known/openid-configuration",
    )
