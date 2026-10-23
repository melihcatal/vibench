import os
from typing import Any, Dict, Optional

import requests


OKTA_USERINFO_URL = "https://{domain}/oauth2/v1/userinfo"


def fetch_and_normalize_profile_claims(access_token: str, okta_domain: Optional[str] = None) -> Dict[str, Any]:
    domain = okta_domain or os.getenv("OKTA_DOMAIN")
    if not domain:
        raise ValueError("OKTA_DOMAIN is required")

    url = OKTA_USERINFO_URL.format(domain=domain)
    response = requests.get(url, headers={"Authorization": f"Bearer {access_token}"}, timeout=10)
    response.raise_for_status()
    claims = response.json()

    return {
        "provider": "okta",
        "subject": claims.get("sub"),
        "email": claims.get("email"),
        "email_verified": claims.get("email_verified"),
        "full_name": claims.get("name"),
        "given_name": claims.get("given_name"),
        "family_name": claims.get("family_name"),
        "preferred_username": claims.get("preferred_username"),
        "locale": claims.get("locale"),
        "raw_claims": claims,
    }


def normalize_profile_claims(claims: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "provider": "okta",
        "subject": claims.get("sub") or claims.get("subject"),
        "email": claims.get("email"),
        "email_verified": claims.get("email_verified"),
        "full_name": claims.get("name") or claims.get("full_name"),
        "given_name": claims.get("given_name"),
        "family_name": claims.get("family_name"),
        "preferred_username": claims.get("preferred_username"),
        "locale": claims.get("locale"),
        "raw_claims": claims,
    }
