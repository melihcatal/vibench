from __future__ import annotations

from authlib.integrations.requests_client import OAuth2Session

from identity_client import load_identity_config
from identity_models import NormalizedProfile, normalize_claims


def fetch_profile_claims(access_token: str) -> NormalizedProfile:
    config = load_identity_config()
    session = OAuth2Session(client_id=config.client_id, token={"access_token": access_token, "token_type": "Bearer"})
    userinfo_endpoint = f"{config.issuer_url.rstrip('/')}/userinfo"
    claims = session.get(userinfo_endpoint).json()
    return normalize_claims(claims)
