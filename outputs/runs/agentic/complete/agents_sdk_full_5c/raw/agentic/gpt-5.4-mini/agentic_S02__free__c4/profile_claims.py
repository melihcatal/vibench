from __future__ import annotations

from typing import Any, Dict

import requests

from identity_client import load_identity_client_config, normalize_claims
from identity_models import FederatedProfile


AUTH0_CLAIM_EMAIL = "email"
AUTH0_CLAIM_NAME = "name"
AUTH0_CLAIM_GIVEN_NAME = "given_name"
AUTH0_CLAIM_FAMILY_NAME = "family_name"
AUTH0_CLAIM_PICTURE = "picture"
AUTH0_CLAIM_SUB = "sub"


def fetch_and_normalize_profile(access_token: str) -> FederatedProfile:
    cfg = load_identity_client_config()
    response = requests.get(
        cfg.userinfo_endpoint,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=15,
    )
    response.raise_for_status()
    raw: Dict[str, Any] = response.json()
    claims = normalize_claims(raw)
    return FederatedProfile(
        provider="auth0",
        subject=str(claims.get(AUTH0_CLAIM_SUB, "")),
        email=claims.get(AUTH0_CLAIM_EMAIL),
        email_verified=claims.get("email_verified"),
        display_name=claims.get(AUTH0_CLAIM_NAME),
        given_name=claims.get(AUTH0_CLAIM_GIVEN_NAME),
        family_name=claims.get(AUTH0_CLAIM_FAMILY_NAME),
        picture=claims.get(AUTH0_CLAIM_PICTURE),
        raw_claims=claims,
    )
