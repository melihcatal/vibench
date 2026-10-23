from typing import Dict, Optional
import msal
import os
import uuid


def start_oauth_login(redirect_uri: str, state: Optional[str] = None) -> Dict[str, str]:
    """
    Start OAuth 2.0 authorization code flow with PKCE for Microsoft Entra ID.
    Returns authorization URL and state for session tracking.
    """
    tenant_id = os.getenv("AZURE_TENANT_ID")
    client_id = os.getenv("AZURE_CLIENT_ID")
    authority = f"https://login.microsoftonline.com/{tenant_id}"

    app = msal.ConfidentialClientApplication(
        client_id=client_id,
        authority=authority,
        client_credential=os.getenv("AZURE_CLIENT_SECRET"),
    )

    if not state:
        state = str(uuid.uuid4())

    auth_url = app.get_authorization_request_url(
        scopes=["openid", "profile", "email"],
        state=state,
        redirect_uri=redirect_uri,
        response_mode="query",
        prompt="select_account",
        code_challenge_method="S256",
    )

    return {"authorization_url": auth_url, "state": state}
