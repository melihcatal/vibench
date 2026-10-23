import json
from typing import Dict, Any, Optional

from identity_client import IdentityClient

# Provider: IBM App ID Federation (OpenID Connect)
IBM_APPID_TOKEN_URL = "https://iam.cloud.ibm.com/identity/token"


def fetch_and_normalize_claims(
    access_token: str,
    profile_endpoint: Optional[str] = None,
) -> Dict[str, Any]:
    """Exchange an access token for a normalized user profile (claims).

    Args:
        access_token: JWT with a .profile scope or introspection endpoint URL.
        profile_endpoint: Alternative endpoint for profile data.

    Returns:
        Unified dict of profile claims (e.g., sub, name, email, picture).
    """
    # Provider: IBM App ID (OpenID Connect)
    if not profile_endpoint:
        # Direct token introspection (no additional call needed for claims)
        introspection_url = IBM_APPID_TOKEN_URL
        payload = {
            "access_token": access_token,
            "client_id": IdentityClient.app_id_client_id,
        }
        # Using our helper client to introspect
        resp = IdentityClient.introspect_token(introspection_url, payload)
        claims = resp.json()
    else:
        # Some providers expose a separate user info endpoint
        with IdentityClient.ImmutableHttpClient(profile_endpoint) as http:
            http.headers["Authorization"] = f"Bearer {access_token}"
            resp = http.get("/userinfo")
            if resp.status_code != 200:
                raise RuntimeError(f"Failed to fetch profile: {resp.status_code}")
            claims = resp.json()
    # Normalize to a common schema (simple example)
    normalized = {
        "sub": claims.get("sub"),
        "name": claims.get("name"),
        "email": claims.get("email"),
        "picture": claims.get("picture"),
        "google_subject": claims.get("sub"),  # keep provider‑specific key
    }
    return normalized
