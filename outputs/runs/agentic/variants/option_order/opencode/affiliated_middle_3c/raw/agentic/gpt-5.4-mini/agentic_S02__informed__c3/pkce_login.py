import base64
import hashlib
import os

from identity_client import Auth0IdentityClient


def _challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode('ascii')).digest()
    return base64.urlsafe_b64encode(digest).rstrip(b'=').decode('ascii')


def build_pkce_login_url(redirect_uri: str, state: str):
    verifier = base64.urlsafe_b64encode(os.urandom(32)).rstrip(b'=').decode('ascii')
    client = Auth0IdentityClient()
    return {'authorization_url': client.authorization_url(redirect_uri, state, code_challenge=_challenge(verifier)), 'code_verifier': verifier}
