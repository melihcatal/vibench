import time
from typing import Any, Dict, List, Optional

import requests

from identity_models import (
    OAuthConfig,
    UserProfile,
    AuditEvent,
    AuditEventType,
)
from identity_client import (
    load_okta_config,
    fetch_user_profile,
    extract_provider_from_issuer,
)


OKTA_ORG_URL = "https://dev-example.okta.com"
OKTA_USERINFO_URL = f"{OKTA_ORG_URL}/oauth2/default/v1/userinfo"
OKTA_API_URL = f"{OKTA_ORG_URL}/api/v1"


def fetch_okta_profile_claims(
    access_token: str,
    config: Optional[OAuthConfig] = None,
) -> Dict[str, Any]:
    if config is None:
        config = load_okta_config()

    profile = fetch_user_profile(config, access_token)
    normalized = profile.normalize()

    audit_event = AuditEvent(
        event_id=f"evt_{int(time.time() * 1000)}",
        event_type=AuditEventType.PROFILE_FETCHED,
        timestamp=time.time(),
        user_id=profile.sub,
        provider="okta",
        details={
            "claims_count": len(profile.raw_claims),
            "has_email": profile.email is not None,
            "email_verified": profile.email_verified,
        },
    )

    return {
        "success": True,
        "provider": "okta",
        "profile": normalized,
        "raw_claims": profile.raw_claims,
        "audit_event": audit_event.to_dict(),
    }


def fetch_okta_user_details(
    access_token: str,
    user_id: str,
    api_token: Optional[str] = None,
) -> Dict[str, Any]:
    import os

    api_token = api_token or os.environ.get("OKTA_API_TOKEN", "")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Accept": "application/json",
    }
    if api_token:
        headers["SSWS"] = api_token

    response = requests.get(
        f"{OKTA_API_URL}/users/{user_id}",
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()
    user_data = response.json()

    return {
        "id": user_data.get("id"),
        "status": user_data.get("status"),
        "created": user_data.get("created"),
        "activated": user_data.get("activated"),
        "status_changed": user_data.get("statusChanged"),
        "last_login": user_data.get("lastLogin"),
        "last_updated": user_data.get("lastUpdated"),
        "profile": user_data.get("profile", {}),
        "credentials": {
            "provider": user_data.get("credentials", {}).get("provider", {}),
        },
    }


def normalize_okta_claims(
    raw_claims: Dict[str, Any],
    claim_mapping: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    default_mapping = {
        "sub": "user_id",
        "email": "email",
        "email_verified": "email_verified",
        "name": "display_name",
        "given_name": "first_name",
        "family_name": "last_name",
        "preferred_username": "username",
        "picture": "avatar_url",
        "locale": "locale",
        "zoneinfo": "timezone",
        "updated_at": "last_updated",
    }

    mapping = claim_mapping or default_mapping
    normalized = {}

    for okta_claim, target_field in mapping.items():
        if okta_claim in raw_claims:
            normalized[target_field] = raw_claims[okta_claim]

    normalized["provider"] = "okta"
    normalized["federated"] = True

    return normalized


def get_okta_groups(
    access_token: str,
    user_id: str,
) -> List[Dict[str, Any]]:
    response = requests.get(
        f"{OKTA_API_URL}/users/{user_id}/groups",
        headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json",
        },
        timeout=30,
    )
    response.raise_for_status()
    groups = response.json()

    return [
        {
            "id": g.get("id"),
            "name": g.get("profile", {}).get("name"),
            "description": g.get("profile", {}).get("description"),
            "type": g.get("type"),
        }
        for g in groups
    ]


def fetch_and_normalize_claims(
    access_token: str,
    provider: str = "okta",
    user_id: Optional[str] = None,
) -> Dict[str, Any]:
    if provider == "okta":
        return fetch_okta_profile_claims(access_token)
    raise ValueError(f"Unsupported provider: {provider}")
