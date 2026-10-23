import os
import requests
from msal import ConfidentialClientApplication
from identity_client import get_oidc_config
from identity_models import TokenResponse

AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
AZURE_CLIENT_SECRET = os.getenv("AZURE_CLIENT_SECRET")
AUTHORITY = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}"
TOKEN_ENDPOINT = f"{AUTHORITY}/oauth2/v2.0/token"


def exchange_code_for_tokens(code: str, redirect_uri: str) -> TokenResponse:
    app = ConfidentialClientApplication(
        client_id=AZURE_CLIENT_ID,
        client_credential=AZURE_CLIENT_SECRET,
        authority=AUTHORITY,
    )
    result = app.acquire_token_by_authorization_code(
        code=code,
        scopes=["openid", "profile", "email"],
        redirect_uri=redirect_uri,
    )
    return TokenResponse(
        access_token=result.get("access_token"),
        id_token=result.get("id_token"),
        refresh_token=result.get("refresh_token"),
        expires_in=result.get("expires_in"),
    )