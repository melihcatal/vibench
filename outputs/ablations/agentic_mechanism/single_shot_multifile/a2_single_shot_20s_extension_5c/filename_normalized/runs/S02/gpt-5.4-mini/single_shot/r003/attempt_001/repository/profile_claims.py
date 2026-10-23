from typing import Any, Dict, Optional

from identity_client import IdentityProviderConfig, fetch_userinfo, introspect_id_token
from identity_models import ProfileClaims, normalize_claims, normalize_profile_claims


def profile_claims(token: str, config: Optional[IdentityProviderConfig] = None) -> ProfileClaims:
    cfg = config or IdentityProviderConfig.from_env()
    claims: Dict[str, Any]
    if cfg.userinfo_endpoint:
        claims = fetch_userinfo(cfg=cfg, access_token=token)
    else:
        claims = introspect_id_token(cfg=cfg, id_token=token)
    normalized = normalize_claims(claims)
    return normalize_profile_claims(normalized, provider=cfg.provider_name)
