import os
import secrets
import hashlib
import base64
from urllib.parse import urlencode

def get_client_config(provider: str) -> dict:
    prefix = provider.upper()
    return {
        'client_id': os.getenv(f'{prefix}_CLIENT_ID'),
        'client_secret': os.getenv(f'{prefix}_CLIENT_SECRET', None),
    }

def generate_pkce_pair() -> tuple[str, str]:
    verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')
    challenge_hash = hashlib.sha256(verifier.encode('utf-8')).digest()
    challenge = base64.urlsafe_b64encode(challenge_hash).decode('utf-8').rstrip('=')
    return verifier, challenge