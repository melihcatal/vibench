import os
import urllib.parse
import base64
import hashlib

# Microsoft Azure AD / OIDC Configuration
AZURE_AD_TENANT_ID = os.environ.get("AZURE_AD_TENANT_ID", "common") # "common" for multi-tenant apps
AZURE_AD_CLIENT_ID = os.environ.get("AZURE_AD_CLIENT_ID", "YOUR_AZURE_AD_CLIENT_ID")
AZURE_AD_REDIRECT_URI = os.environ.get("AZURE_AD_REDIRECT_URI", "http://localhost:8000/oauth_callback")
AZURE_AD_AUTHORITY = f"https://login.microsoftonline.com/{AZURE_AD_TENANT_ID}"
AZURE_AD_AUTH_ENDPOINT = f"{AZURE_AD_AUTHORITY}/oauth2/v2.0/authorize"
AZURE_AD_TOKEN_ENDPOINT = f"{AZURE_AD_AUTHORITY}/oauth2/v2.0/token"
AZURE_AD_GRAPH_ENDPOINT = "https://graph.microsoft.com/v1.0/me"

# Scopes required for the application
AZURE_AD_SCOPES = [
    "openid",
    "profile",
    "email",
    "offline_access",
    "User.Read", # Microsoft Graph scope for user profile
]

def generate_pkce_codes():
    """Generates PKCE code_verifier and code_challenge."""
    code_verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')
    # S256 code_challenge
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode('utf-8')).digest()
    ).rstrip(b'=').decode('utf-8')
    return code_verifier, code_challenge

def build_auth_url(scopes: list, response_type: str = "code", code_challenge: str = None, code_challenge_method: str = None):
    """Builds the Azure AD authorization URL."""
    params = {
        "client_id": AZURE_AD_CLIENT_ID,
        "response_type": response_type,
        "redirect_uri": AZURE_AD_REDIRECT_URI,
        "scope": " ".join(scopes),
        "response_mode": "query",
        "prompt": "select_account",
    }
    if code_challenge and code_challenge_method:
        params["code_challenge"] = code_challenge
        params["code_challenge_method"] = code_challenge_method
    return f"{AZURE_AD_AUTH_ENDPOINT}?{urllib.parse.urlencode(params)}"
