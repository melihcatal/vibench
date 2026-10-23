from identity_client import Auth0IdentityClient
from identity_models import CallbackRequest


def handle_oauth_callback(code: str, state: str, redirect_uri: str, code_verifier: str | None = None):
    client = Auth0IdentityClient()
    req = CallbackRequest(code=code, state=state, redirect_uri=redirect_uri, code_verifier=code_verifier)
    return client.exchange_code(req.code, req.redirect_uri, req.code_verifier).to_dict()
