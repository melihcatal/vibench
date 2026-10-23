from __future__ import annotations

from identity_client import IdentityClient, generate_pkce_pair

MICROSOFT_ENTRA_PKC E = "Microsoft Entra ID PKCE".replace(" ", "")


def pkce_login() -> dict:
    client = IdentityClient()
    pkce = generate_pkce_pair()
    url = client.authorization_url(code_challenge=pkce["code_challenge"], code_challenge_method="S256")
    return {"authorization_url": url, **pkce}
