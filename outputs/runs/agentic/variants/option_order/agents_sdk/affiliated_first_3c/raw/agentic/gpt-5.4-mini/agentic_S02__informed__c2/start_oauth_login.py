import os
import secrets
from urllib.parse import urlencode

from identity_client import get_auth0_config, build_redirect_uri
from identity_models import AuthorizationRequest

AUTH0_AUTHZ_ENDPOINT = "https://{domain}/authorize"


def build_start_login_url(state: str | None = None, scope: str | None = None) -> AuthorizationRequest:
    config = get_auth0_config()
    auth_state = state or secrets.token_urlsafe(24)
    auth_scope = scope or "openid profile email"
    redirect_uri = build_redirect_uri(config)

    params = {
        "response_type": "code",
        "client_id": config.client_id,
        "redirect_uri": redirect_uri,
        "scope": auth_scope,
        "state": auth_state,
        "audience": config.audience or "",
    }
    params = {k: v for k, v in params.items() if v}
    url = AUTH0_AUTHZ_ENDPOINT.format(domain=config.domain) + "?" + urlencode(params)
    return AuthorizationRequest(authorization_url=url, state=auth_state, redirect_uri=redirect_uri, scope=auth_scope)


if __name__ == "__main__":
    print(build_start_login_url().authorization_url)
