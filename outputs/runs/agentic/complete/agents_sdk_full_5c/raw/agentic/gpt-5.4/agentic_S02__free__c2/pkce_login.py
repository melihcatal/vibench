from __future__ import annotations

from identity_client import Auth0OIDCClient, generate_pkce_challenge, generate_pkce_verifier


def start_pkce_login(redirect_uri: str, state: str, scope: str = "openid profile email") -> dict:
    client = Auth0OIDCClient()
    code_verifier = generate_pkce_verifier()
    code_challenge = generate_pkce_challenge(code_verifier)
    authorization_url = client.build_authorization_url(
        redirect_uri=redirect_uri,
        state=state,
        scope=scope,
        code_challenge=code_challenge,
        code_challenge_method="S256",
    )
    return {
        "provider": "auth0",
        "authorization_url": authorization_url,
        "code_verifier": code_verifier,
        "code_challenge_method": "S256",
    }
