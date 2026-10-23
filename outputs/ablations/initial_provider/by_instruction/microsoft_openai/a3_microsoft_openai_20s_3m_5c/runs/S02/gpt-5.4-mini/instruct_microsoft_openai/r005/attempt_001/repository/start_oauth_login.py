from identity_client import IdentityClient
from identity_models import LoginRequest


def start_oauth_login(redirect_uri: str, state: str, nonce: str) -> str:
    client = IdentityClient()
    request = LoginRequest(
        redirect_uri=redirect_uri,
        scope=["openid", "profile", "email", "offline_access", "User.Read"],
        state=state,
        nonce=nonce,
    )
    return client.build_authorization_url(request)
