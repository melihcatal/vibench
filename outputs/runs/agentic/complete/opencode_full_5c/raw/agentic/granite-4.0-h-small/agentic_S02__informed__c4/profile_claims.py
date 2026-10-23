import os
from identity_client import IdentityClient


def profile_claims(access_token):
    """Retrieve and normalize the federated user profile claims.
    Uses Alibaba Cloud IDaaS EIAM OIDC as the concrete provider.
    Returns a dict with common keys: sub, name, email, picture, locale, updated_at.
    """
    client = IdentityClient()
    # Alibaba IDaaS token introspection endpoint returns a JWT with claims
    introspect_resp = client.introspect_token(access_token)
    if not introspect_resp.ok:
        raise RuntimeError(f"Token introspection failed: {introspect_resp.text}")

    claims = introspect_resp.json()
    # Normalize to OIDC standard claim names
    normalized = {
        "sub": claims.get("sub"),
        "name": claims.get("name"),
        "email": claims.get("email"),
        "picture": claims.get("picture"),
        "locale": claims.get("locale"),
        "updated_at": claims.get("updated_at"),
    }
    return normalized


if __name__ == "__main__":
    # Example: fetch claims using a mock access token
    mock_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    print(profile_claims(mock_token))
