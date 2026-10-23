from __future__ import annotations

from identity_client import Auth0IdentityClient, create_code_challenge, create_code_verifier
from identity_models import FederatedLoginRequest


def build_pkce_login_url() -> tuple[str, str]:
    client = Auth0IdentityClient()
    verifier = create_code_verifier()
    challenge = create_code_challenge(verifier)
    request = FederatedLoginRequest(
        issuer=f"https://{client.domain}/",
        client_id=client.client_id,
        redirect_uri="https://localhost/callback",
        code_challenge=challenge,
        code_challenge_method="S256",
    )
    return client.build_login_url(request), verifier
