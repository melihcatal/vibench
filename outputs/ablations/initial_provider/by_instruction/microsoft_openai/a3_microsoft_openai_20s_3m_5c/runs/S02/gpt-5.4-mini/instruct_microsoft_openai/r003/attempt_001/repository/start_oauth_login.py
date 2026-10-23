from identity_client import build_authorization_url
from identity_models import OAuthLoginRequest


def start_login(redirect_uri: str, state: str = None, code_challenge: str = None) -> str:
    request = OAuthLoginRequest(redirect_uri=redirect_uri, state=state)
    return build_authorization_url(request, code_challenge=code_challenge)
