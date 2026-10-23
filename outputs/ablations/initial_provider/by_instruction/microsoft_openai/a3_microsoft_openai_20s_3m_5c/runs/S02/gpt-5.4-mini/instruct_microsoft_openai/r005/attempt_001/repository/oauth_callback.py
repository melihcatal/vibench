from typing import Optional

from identity_client import IdentityClient


def oauth_callback(code: str, redirect_uri: str, code_verifier: Optional[str] = None):
    client = IdentityClient()
    return client.exchange_code(code=code, redirect_uri=redirect_uri, code_verifier=code_verifier)
