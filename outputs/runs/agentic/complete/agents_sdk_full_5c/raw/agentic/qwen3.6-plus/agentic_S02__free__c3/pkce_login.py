"""
pkce_login.py - Implements a PKCE (Proof Key for Code Exchange) login flow
for public clients using Auth0 as the identity provider.
"""

from __future__ import annotations

import json
import logging
from urllib.parse import parse_qs

from identity_client import (
    AUTH0_DOMAIN,
    AUTH0_CLIENT_ID,
    AUTH0_REDIRECT_URI,
    AUTH0_SCOPE,
    AUTH0_AUDIENCE,
    build_auth_url,
    exchange_code_for_tokens,
    generate_code_challenge,
    generate_code_verifier,
    generate_state,
    save_state,
)
from identity_models import AuthRequest, TokenResponse

logger = logging.getLogger(__name__)


class PKCELoginFlow:
    """Manages a full PKCE authorization-code flow against Auth0."""

    def __init__(
        self,
        domain: str = AUTH0_DOMAIN,
        client_id: str = AUTH0_CLIENT_ID,
        redirect_uri: str = AUTH0_REDIRECT_URI,
        scope: str = AUTH0_SCOPE,
        audience: str | None = AUTH0_AUDIENCE,
    ):
        self.domain = domain
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.audience = audience
        self._verifier: str | None = None
        self._state: str | None = None

    def start(self, request: AuthRequest | None = None) -> dict[str, str]:
        """
        Start the PKCE flow: generate code verifier/challenge, build the
        authorization URL, and save state for callback.
        """
        self._verifier = generate_code_verifier()
        challenge = generate_code_challenge(self._verifier)
        self._state = generate_state()

        req = request or AuthRequest(redirect_uri=self.redirect_uri, scope=self.scope)

        auth_url = build_auth_url(
            domain=self.domain,
            client_id=self.client_id,
            redirect_uri=req.redirect_uri,
            scope=req.scope,
            state=self._state,
            code_challenge=challenge,
            code_challenge_method="S256",
            audience=req.audience or self.audience,
        )

        save_state(self._state, {
            "verifier": self._verifier,
            "redirect_uri": req.redirect_uri,
            "audience": req.audience or self.audience,
            "scope": req.scope,
        })

        logger.info("PKCE flow started via auth0, state=%s", self._state)
        return {"auth_url": auth_url, "state": self._state}

    def complete(self, code: str, state: str) -> TokenResponse:
        """
        Complete the PKCE flow by exchanging the authorization code for
        tokens at the Auth0 /oauth/token endpoint with the code_verifier.
        """
        if state != self._state:
            stored = save_state.__self__._state_store.get(state)
            if stored is None:
                raise ValueError("Invalid or expired PKCE state")
            verifier = stored.get("verifier")
            redirect_uri = stored.get("redirect_uri", self.redirect_uri)
            audience = stored.get("audience", self.audience)
        else:
            verifier = self._verifier
            redirect_uri = self.redirect_uri
            audience = self.audience

        if not verifier:
            raise ValueError("No code verifier available for PKCE exchange")

        token_data = exchange_code_for_tokens(
            code=code,
            domain=self.domain,
            client_id=self.client_id,
            client_secret="",
            redirect_uri=redirect_uri,
            code_verifier=verifier,
            audience=audience,
        )

        response = TokenResponse.from_raw(token_data)
        logger.info("PKCE token exchange succeeded via auth0, state=%s", state)
        return response


def init_pkce_login(
    domain: str = AUTH0_DOMAIN,
    client_id: str = AUTH0_CLIENT_ID,
    redirect_uri: str = AUTH0_REDIRECT_URI,
    scope: str = AUTH0_SCOPE,
    audience: str | None = AUTH0_AUDIENCE,
) -> PKCELoginFlow:
    """Factory to create a PKCELoginFlow instance targeting Auth0."""
    return PKCELoginFlow(
        domain=domain,
        client_id=client_id,
        redirect_uri=redirect_uri,
        scope=scope,
        audience=audience,
    )


if __name__ == "__main__":
    flow = init_pkce_login()
    result = flow.start()
    print(json.dumps(result, indent=2))
