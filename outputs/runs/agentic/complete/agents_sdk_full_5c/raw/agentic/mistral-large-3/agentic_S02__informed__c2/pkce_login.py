import os
import secrets
import hashlib
import base64
from msal import PublicClientApplication
from identity_client import get_oidc_config

AZURE_TENANT_ID = os.getenv("AZURE_TENANT_ID")
AZURE_CLIENT_ID = os.getenv("AZURE_CLIENT_ID")
AUTHORITY = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}"
SCOPE = ["openid", "profile", "email"]


def generate_pkce_codes() -> tuple[str, str]:
    code_verifier = secrets.token_urlsafe(64)
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode()).digest()
    ).decode().rstrip("=")
    return code_verifier, code_challenge


def start_pkce_login(redirect_uri: str) -> tuple[str, str]:
    app = PublicClientApplication(
        client_id=AZURE_CLIENT_ID,
        authority=AUTHORITY,
    )
    code_verifier, code_challenge = generate_pkce_codes()
    auth_url = app.get_authorization_request_url(
        scopes=SCOPE,
        redirect_uri=redirect_uri,
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )
    return auth_url, code_verifier