from identity_client import exchange_code
from identity_models import TokenResponse


def oauth_callback(code: str, redirect_uri: str, code_verifier: str = '') -> TokenResponse:
    return exchange_code(code=code, redirect_uri=redirect_uri, code_verifier=code_verifier or None)
