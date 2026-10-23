from typing import Dict, Optional
import msal
import os
import uuid
import hashlib
import base64


def generate_pkce_codes() -> Dict[str, str]:
    """
    Generate PKCE code verifier and challenge for Microsoft Entra ID.
    """
    verifier = base64.urlsafe_b64encode(os.urandom(32)).decode("utf-8").rstrip("=")
    challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(verifier.encode("utf-8")).digest())
        .decode("utf-8")
        .rstrip("=")
    )

    return {"code_verifier": verifier, "code_challenge": challenge}


def start_pkce_login(redirect_uri: str, state: Optional[str] = None) -> Dict[str, str]:
    """
    Start PKCE login flow for Microsoft Entra ID.
    Returns authorization URL, state, and code verifier for session tracking.
    """
    tenant_id = os.getenv("AZURE_TENANT_ID")
    client_id = os.getenv("AZURE_CLIENT_ID")
    authority = f"https://login.microsoftonline.com/{tenant_id}"

    if not state:
        state = str(uuid.uuid4())

    pkce_codes = generate_pkce_codes()

    app = msal.PublicClientApplication(client_id=client_id, authority=authority)

    auth_url = app.get_authorization_request_url(
        scopes=["openid", "profile", "email"],
        state=state,
        redirect_uri=redirect_uri,
        response_mode="query",
        prompt="select_account",
        code_challenge=pkce_codes["code_challenge"],
        code_challenge_method="S256",
    )

    return {
        "authorization_url": auth_url,
        "state": state,
        "code_verifier": pkce_codes["code_verifier"],
    }
