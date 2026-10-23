import os
import requests
from typing import Optional, Dict, Any, List
from identity_models import (
    OAuthConfig,
    UserProfile,
    AuditEvent,
    AuditEventType,
    build_audit_event,
    normalize_claims,
)
from identity_client import (
    load_auth0_config,
    fetch_user_profile,
    decode_id_token_claims,
)


def fetch_profile_claims(
    access_token: str,
    config: Optional[OAuthConfig] = None,
    id_token: Optional[str] = None,
    ip_address: Optional[str] = None,
    user_agent: Optional[str] = None,
) -> Dict[str, Any]:
    if config is None:
        config = load_auth0_config()

    userinfo_profile = fetch_user_profile(config=config, access_token=access_token)

    id_token_claims = {}
    if id_token:
        try:
            id_token_claims = decode_id_token_claims(id_token)
        except Exception:
            id_token_claims = {}

    merged_claims = {**userinfo_profile.raw_claims, **id_token_claims}
    normalized_profile = normalize_claims(merged_claims)

    audit_event = build_audit_event(
        event_type=AuditEventType.PROFILE_FETCHED,
        user_sub=normalized_profile.sub,
        provider="auth0",
        status="success",
        details={
            "userinfo_endpoint": config.userinfo_endpoint,
            "claims_count": len(merged_claims),
            "has_id_token_claims": bool(id_token_claims),
        },
        ip_address=ip_address,
        user_agent=user_agent,
    )

    return {
        "success": True,
        "profile": normalized_profile.to_dict(),
        "merged_claims": merged_claims,
        "audit_event": audit_event.to_dict(),
    }


def normalize_federated_profile(
    raw_claims: Dict[str, Any],
    provider: str = "auth0",
) -> UserProfile:
    normalized = normalize_claims(raw_claims)

    if provider == "auth0":
        if "nickname" in raw_claims and not normalized.name:
            normalized.name = raw_claims["nickname"]
        if "identities" in raw_claims:
            identities = raw_claims["identities"]
            if isinstance(identities, list) and len(identities) > 0:
                primary_identity = identities[0]
                normalized.raw_claims["primary_connection"] = primary_identity.get(
                    "connection"
                )
                normalized.raw_claims["primary_provider"] = primary_identity.get(
                    "provider"
                )

    return normalized


def extract_email_from_claims(claims: Dict[str, Any]) -> Optional[str]:
    for key in ["email", "preferred_username", "upn", "mail"]:
        if key in claims and claims[key]:
            return claims[key]
    return None


def extract_name_from_claims(claims: Dict[str, Any]) -> Optional[str]:
    for key in ["name", "nickname", "preferred_username", "displayName"]:
        if key in claims and claims[key]:
            return claims[key]
    return None


def get_auth0_user_roles(
    access_token: str, config: Optional[OAuthConfig] = None
) -> List[str]:
    if config is None:
        config = load_auth0_config()

    response = requests.get(
        config.userinfo_endpoint,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30,
    )
    response.raise_for_status()
    claims = response.json()

    roles = claims.get("roles", [])
    if isinstance(roles, list):
        return roles
    return []


def fetch_auth0_user_metadata(
    access_token: str,
    config: Optional[OAuthConfig] = None,
) -> Dict[str, Any]:
    if config is None:
        config = load_auth0_config()

    response = requests.get(
        config.userinfo_endpoint,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=30,
    )
    response.raise_for_status()
    claims = response.json()

    metadata = {
        "app_metadata": claims.get("app_metadata", {}),
        "user_metadata": claims.get("user_metadata", {}),
    }
    return metadata
