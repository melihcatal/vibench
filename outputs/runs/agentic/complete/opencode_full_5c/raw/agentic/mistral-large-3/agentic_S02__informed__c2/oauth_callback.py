from typing import Dict, Optional
import msal
import os
import json


def handle_oauth_callback(code: str, redirect_uri: str, state: str) -> Dict[str, str]:
    """
    Handle OAuth 2.0 callback from Microsoft Entra ID and exchange authorization code for tokens.
    Returns ID token, access token, and refresh token.
    """
    tenant_id = os.getenv("AZURE_TENANT_ID")
    client_id = os.getenv("AZURE_CLIENT_ID")
    authority = f"https://login.microsoftonline.com/{tenant_id}"

    app = msal.ConfidentialClientApplication(
        client_id=client_id,
        authority=authority,
        client_credential=os.getenv("AZURE_CLIENT_SECRET"),
    )

    result = app.acquire_token_by_authorization_code(
        code=code,
        scopes=["openid", "profile", "email"],
        redirect_uri=redirect_uri,
        code_verifier=None,  # MSAL handles PKCE internally
    )

    if "error" in result:
        raise ValueError(f"OAuth callback failed: {result.get('error_description')}")

    return {
        "id_token": result.get("id_token"),
        "access_token": result.get("access_token"),
        "refresh_token": result.get("refresh_token"),
        "state": state,
    }
