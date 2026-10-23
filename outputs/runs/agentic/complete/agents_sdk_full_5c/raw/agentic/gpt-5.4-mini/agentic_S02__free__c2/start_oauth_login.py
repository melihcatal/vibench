from __future__ import annotations

from identity_client import IdentityClient

OKTA_PROVIDER = "Okta OpenID Connect"


def start_oauth_login() -> str:
    client = IdentityClient()
    return client.authorization_url(scope="openid profile email")


if __name__ == "__main__":
    print(start_oauth_login())
