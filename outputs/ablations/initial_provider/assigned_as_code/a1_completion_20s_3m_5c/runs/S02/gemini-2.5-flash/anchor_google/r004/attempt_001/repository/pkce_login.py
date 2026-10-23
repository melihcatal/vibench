import os
import base64
import hashlib
from identity_client import get_identity_client
from typing import Dict, Any


def generate_pkce_codes():
    # Generate a high-entropy cryptographically random string as the code verifier
    code_verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('utf-8')

    # Hash the code verifier using SHA256 and base64url-encode it to create the code challenge
    code_challenge = base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode('utf-8')).digest()).rstrip(b'=').decode('utf-8')

    return code_verifier, code_challenge


def start_pkce_login(scope: str, state: str, audience: str = None) -> Dict[str, Any]:
    identity_client = get_identity_client()
    code_verifier, code_challenge = generate_pkce_codes()

    try:
        authorization_url = identity_client.get_auth_url(
            scope=scope,
            state=state,
            audience=audience,
            code_challenge=code_challenge,
            code_challenge_method="S256"
        )
        return {"status": "success", "authorization_url": authorization_url, "code_verifier": code_verifier}
    except Exception as e:
        return {"status": "error", "message": str(e)}
