import os
import secrets
import hashlib
import base64
from typing import Dict

def get_config() -> Dict[str, str]:
    tenant_id = os.getenv('AZURE_TENANT_ID')
    client_id = os.getenv('AZURE_CLIENT_ID')
    client_secret = os.getenv('AZURE_CLIENT_SECRET', '')
    return {
        'tenant_id': tenant_id,
        'client_id': client_id,
        'client_secret': client_secret,
        'authority': f"https://login.microsoftonline.com/{tenant_id}/v2.0",
        'token_endpoint': f"https://login.microsoftonline.com/{tenant_id}/v2.0/token",
        'userinfo_endpoint': 'https://graph.microsoft.com/oidc/userinfo',
        'scopes': 'openid profile email',
    }

def generate_pkce_pair() -> tuple[str, str]:
    verifier_bytes = secrets.token_bytes(32)
    verifier = base64.urlsafe_b64encode(verifier_bytes).decode('utf-8').rstrip('=')
    challenge_bytes = hashlib.sha256(verifier.encode('utf-8')).digest()
    challenge = base64.urlsafe_b64encode(challenge_bytes).decode('utf-8').rstrip('=')
    return verifier, challenge