from identity_client import Auth0IdentityClient
from identity_models import LoginRequest


def build_start_login_url(redirect_uri: str, state: str) -> str:
    client = Auth0IdentityClient()
    req = LoginRequest(redirect_uri=redirect_uri, state=state)
    return client.authorization_url(req.redirect_uri, req.state, req.scope)
