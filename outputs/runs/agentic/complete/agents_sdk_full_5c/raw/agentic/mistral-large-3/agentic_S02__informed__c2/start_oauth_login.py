import os
from msal import ConfidentialClientApplication
from identity_client import get_oidc_config

AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
AUTHORITY = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}"
SCOPE = ["openid", "profile", "email"]


def start_oauth_login(redirect_uri: str) -> str:
    app = ConfidentialClientApplication(
        client_id=AZURE_CLIENT_ID,
        client_credential=AZURE_CLIENT_SECRET,
        authority=AUTHORITY,
    )
    auth_url = app.get_authorization_request_url(
        scopes=SCOPE,
        redirect_uri=redirect_uri,
    )
    return auth_url