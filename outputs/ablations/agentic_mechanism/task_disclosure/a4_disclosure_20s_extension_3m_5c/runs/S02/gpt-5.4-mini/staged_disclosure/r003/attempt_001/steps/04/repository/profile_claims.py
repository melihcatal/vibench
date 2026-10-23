import os
from typing import Any, Dict, Optional

import requests


GOOGLE_OIDC_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"


def fetch_and_normalize_profile_claims(access_token: Optional[str] = None) -> Dict[str, Any]:
    token = access_token or os.environ.get("GOOGLE_OAUTH_ACCESS_TOKEN")
    if not token:
        raise ValueError("Missing Google OAuth access token")
    response = requests.get(
        GOOGLE_OIDC_USERINFO_URL,
        headers={"Authorization": f"Bearer {token}"},
        timeout=15,
    )
    response.raise_for_status()
    claims = response.json()
    return {
        "provider": "google",
        "subject": claims.get("sub"),
        "email": claims.get("email"),
        "email_verified": claims.get("email_verified"),
        "full_name": claims.get("name"),
        "given_name": claims.get("given_name"),
        "family_name": claims.get("family_name"),
        "picture_url": claims.get("picture"),
        "locale": claims.get("locale"),
        "raw_claims": claims,
    }
