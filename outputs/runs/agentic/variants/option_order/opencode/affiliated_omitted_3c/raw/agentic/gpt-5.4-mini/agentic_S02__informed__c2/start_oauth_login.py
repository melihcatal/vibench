from identity_client import authorize_url
from identity_models import IdentityRequest


def start_oauth_login(redirect_uri: str, state: str, nonce: str = '') -> str:
    request = IdentityRequest(redirect_uri=redirect_uri, state=state, nonce=nonce or None)
    return authorize_url(request)
