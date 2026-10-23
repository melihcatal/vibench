from typing import Any, Dict

from identity_client import userinfo
from identity_models import NormalizedProfile, normalize_claims


def profile_claims(access_token: str) -> NormalizedProfile:
    claims: Dict[str, Any] = userinfo(access_token)
    return normalize_claims('auth0', claims)
