from __future__ import annotations

from identity_client import Auth0IdentityClient, build_request


def start_oauth_login() -> str:
    client = Auth0IdentityClient()
    request = build_request()
    return client.build_login_url(request)
