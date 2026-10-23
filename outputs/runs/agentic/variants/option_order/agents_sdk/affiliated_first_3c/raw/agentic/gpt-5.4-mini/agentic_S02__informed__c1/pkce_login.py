from __future__ import annotations

from identity_client import build_auth0_client, generate_nonce, generate_pkce_pair, generate_state
from identity_models import OAuthAuthorizationRequest


def start_pkce_login(redirect_uri: str, scope: str = "openid profile email") -> dict[str, str]:
    client = build_auth0_client()
    code_verifier, code_challenge = generate_pkce_pair()
    request = OAuthAuthorizationRequest(
        redirect_uri=redirect_uri,
        state=generate_state(),
        nonce=generate_nonce(),
        scope=scope,
        extra_params={"prompt": "login"},
    )
    authorization_url = client.build_authorization_url(request, code_challenge=code_challenge)
    return {
        "authorization_url": authorization_url,
        "code_verifier": code_verifier,
        "code_challenge": code_challenge,
    }
