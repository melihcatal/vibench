"""
start_oauth_login.py - Starts an OAuth/OIDC authorization-code login flow
against Auth0.
"""

from __future__ import annotations

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

from identity_client import (
    AUTH0_DOMAIN,
    AUTH0_CLIENT_ID,
    AUTH0_REDIRECT_URI,
    AUTH0_SCOPE,
    build_auth_url,
    generate_state,
    save_state,
)
from identity_models import AuthRequest


def initiate_oauth_login(
    request: AuthRequest | None = None,
    domain: str = AUTH0_DOMAIN,
    client_id: str = AUTH0_CLIENT_ID,
    redirect_uri: str = AUTH0_REDIRECT_URI,
    scope: str = AUTH0_SCOPE,
) -> dict[str, str]:
    """
    Initiate the OAuth 2.0 authorization-code login flow with Auth0.

    Returns a dict with the authorization URL and the generated state.
    """
    if request is None:
        request = AuthRequest(redirect_uri=redirect_uri, scope=scope)

    state = generate_state()
    save_state(state, {
        "redirect_uri": request.redirect_uri,
        "scope": request.scope,
        "audience": request.audience,
    })

    auth_url = build_auth_url(
        domain=domain,
        client_id=client_id,
        redirect_uri=request.redirect_uri,
        scope=request.scope,
        state=state,
        connection=request.connection,
        audience=request.audience,
        extra_params=request.extra_params,
    )

    return {"auth_url": auth_url, "state": state}


class OAuthLoginHandler(BaseHTTPRequestHandler):
    """Minimal HTTP handler that starts an Auth0 authorization-code flow."""

    def do_GET(self) -> None:
        if self.path.startswith("/login"):
            query = parse_qs(self.path.split("?", 1)[-1]) if "?" in self.path else {}
            request = AuthRequest(
                redirect_uri=query.get("redirect_uri", [AUTH0_REDIRECT_URI])[0],
                scope=query.get("scope", [AUTH0_SCOPE])[0],
                connection=query.get("connection", [None])[0],
                audience=query.get("audience", [None])[0],
            )
            result = initiate_oauth_login(
                request=request,
                redirect_uri=request.redirect_uri,
                scope=request.scope,
            )
            self.send_response(302)
            self.send_header("Location", result["auth_url"])
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()


if __name__ == "__main__":
    result = initiate_oauth_login()
    print(json.dumps(result, indent=2))
