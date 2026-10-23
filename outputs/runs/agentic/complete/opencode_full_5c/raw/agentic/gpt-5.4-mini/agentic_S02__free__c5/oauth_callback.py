from identity_client import exchange_auth_code
from identity_models import TokenExchangeRequest


def handle_oauth_callback(request: TokenExchangeRequest):
    return exchange_auth_code(request.code, request.redirect_uri, request.code_verifier)
