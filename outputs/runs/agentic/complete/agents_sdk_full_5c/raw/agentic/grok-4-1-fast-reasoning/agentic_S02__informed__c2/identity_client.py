import os
import secrets
from hashlib import pbkdf2_hmac
import base64

AZURE_TENANT_ID = os.getenv('AZURE_TENANT_ID')
AZURE_CLIENT_ID = os.getenv('AZURE_CLIENT_ID')
AUTHORITY = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/v2.0"
USERINFO_ENDPOINT = f"https://login.microsoftonline.com/{AZURE_TENANT_ID}/v2.0/userinfo"
SCOPES = ["openid", "profile", "email"]
REDIRECT_URI = "http://localhost:8080/callback"
CONFIG = {
    "tenant_id": AZURE_TENANT_ID,
    "client_id": AZURE_CLIENT_ID,
    "authority": AUTHORITY,
    "userinfo_endpoint": USERINFO_ENDPOINT,
    "scopes": SCOPES,
    "redirect_uri": REDIRECT_URI,
}

def get_config():
    return CONFIG

def generate_state():
    return secrets.token_urlsafe(32)

def generate_pkce_pair():
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')
    challenge_bytes = pbkdf2_hmac('sha256', verifier.encode('ascii'), b'', 60000)
    challenge = base64.urlsafe_b64encode(challenge_bytes).decode('utf-8').rstrip('=')
    return verifier, challenge