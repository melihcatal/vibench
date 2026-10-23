import os
from urllib.parse import urlencode
import base64
import hashlib

class IdentityClientConfig:
    AZURE_AD_TENANT_ID = os.environ.get("AZURE_AD_TENANT_ID", "common") # "common" for multi-tenant apps
    AZURE_AD_CLIENT_ID = os.environ.get("AZURE_AD_CLIENT_ID")
    AZURE_AD_CLIENT_SECRET = os.environ.get("AZURE_AD_CLIENT_SECRET")
    AZURE_AD_AUTHORITY = f"https://login.microsoftonline.com/{AZURE_AD_TENANT_ID}"
    AZURE_AD_AUTHORIZE_ENDPOINT = f"{AZURE_AD_AUTHORITY}/oauth2/v2.0/authorize"
    AZURE_AD_TOKEN_ENDPOINT = f"{AZURE_AD_AUTHORITY}/oauth2/v2.0/token"
    AZURE_AD_GRAPH_ENDPOINT = "https://graph.microsoft.com/v1.0/me"

    REDIRECT_URI = os.environ.get("REDIRECT_URI", "http://localhost:8000/oauth/callback")

def generate_pkce_challenge():
    code_verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')
    hashed = hashlib.sha256(code_verifier.encode('utf-8')).digest()
    code_challenge = base64.urlsafe_b64encode(hashed).rstrip(b'=').decode('utf-8')
    return code_verifier, code_challenge

def build_authorization_url(
    client_id: str,
    redirect_uri: str,
    scope: str,
    state: str,
    response_type: str = "code",
    code_challenge: Optional[str] = None,
    code_challenge_method: Optional[str] = None
) -> str:
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "response_type": response_type,
        "state": state,
    }
    if code_challenge:
        params["code_challenge"] = code_challenge
        params["code_challenge_method"] = code_challenge_method

    return f"{IdentityClientConfig.AZURE_AD_AUTHORIZE_ENDPOINT}?{urlencode(params)}"
