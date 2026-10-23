import os
import secrets

from identity_client import AUTH0_REDIRECT_URI, build_authorization_url
from identity_models import OAuthRequest


def start_login(
    redirect_uri: str = AUTH0_REDIRECT_URI, scope: str = "openid profile email"
) -> str:
    request = OAuthRequest(
        redirect_uri=redirect_uri, state=secrets.token_urlsafe(24), scope=scope
    )
    return build_authorization_url(request)


if __name__ == "__main__":
    print(start_login())
