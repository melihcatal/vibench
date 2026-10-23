import os
import base64
import requests
from identity_client import IdentityClient

# Auth0 PKCE flow (swap for Google, Cognito, etc. by changing endpoints)
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
REDIRECT_URI = 'http://localhost:8000/oauth_callback'

# Helper to generate PKCE code_verifier and challenge
def _generate_pkce_pair() -> (str, str):
    import secrets, hashlib
    verifier = secrets.token_urlsafe(32)
    verifier_bytes = verifier.encode('utf-8')
    challenge_bytes = hashlib.sha256(verifier_bytes).digest()
    challenge = base64.urlsafe_b64encode(challenge_bytes).rstrip(b'=').decode('utf-8')
    return verifier, challenge


def start_pkce_login():
    verifier, code_challenge = _generate_pkce_pair()

    auth_url = (
        f"https://{AUTH0_DOMAIN}/authorize?"
        f"response_type=code&"
        f"client_id={AUTH0_CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"scope=openid%20profile%20email&"
        f"code_challenge={code_challenge}&"
        f"code_challenge_method=S256"
    )

    print('Open this URL to authenticate:')
    print(auth_url)
    # In a real app the user would be redirected back to REDIRECT_URI
    # After the redirect, oauth_callback.py will receive `code` and `code_verifier`
    # to exchange for tokens.

if __name__ == '__main__':
    start_pkce_login()
