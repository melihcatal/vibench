from __future__ import annotations

from typing import Any, Dict

from identity_client import AUTH0_DOMAIN, fetch_auth0_userinfo, normalize_auth0_profile


def profile_claims(access_token: str) -> Dict[str, Any]:
    userinfo = fetch_auth0_userinfo(AUTH0_DOMAIN, access_token)
    profile = normalize_auth0_profile(userinfo)
    return {
        "subject": profile.subject,
        "email": profile.email,
        "display_name": profile.display_name,
        "given_name": profile.given_name,
        "family_name": profile.family_name,
        "issuer": profile.issuer,
        "raw": profile.raw,
    }
