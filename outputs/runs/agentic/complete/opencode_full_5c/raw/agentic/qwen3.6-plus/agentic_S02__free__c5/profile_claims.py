import os
from typing import Optional

import requests

from identity_client import get_config, IdentityConfig, fetch_userinfo
from identity_models import NormalizedProfile, AuditRecord, AuditEventType


PROVIDER = "auth0"
AUTH0_USERINFO_ENDPOINT = "https://{domain}/userinfo"
AUTH0_API_ENDPOINT = "https://{domain}/api/v2"


def fetch_and_normalize_profile(
    access_token: str,
    session_id: Optional[str] = None,
    config: Optional[IdentityConfig] = None,
) -> dict:
    cfg = config or get_config()
    raw_claims = fetch_userinfo(access_token=access_token, config=cfg)
    profile = NormalizedProfile.from_auth0_claims(raw_claims)
    audit_record = AuditRecord(
        event_type=AuditEventType.PROFILE_FETCHED,
        session_id=session_id,
        user_id=profile.sub,
        provider=PROVIDER,
        details={
            "email": profile.email,
            "email_verified": profile.email_verified,
        },
    )
    return {
        "profile": {
            "sub": profile.sub,
            "email": profile.email,
            "email_verified": profile.email_verified,
            "name": profile.name,
            "given_name": profile.given_name,
            "family_name": profile.family_name,
            "picture": profile.picture,
            "locale": profile.locale,
            "phone_number": profile.phone_number,
            "phone_number_verified": profile.phone_number_verified,
            "provider": profile.provider,
            "provider_id": profile.provider_id,
        },
        "audit_record": audit_record.to_dict(),
    }


def fetch_user_metadata(
    user_id: str,
    management_api_token: str,
    config: Optional[IdentityConfig] = None,
) -> dict:
    cfg = config or get_config()
    api_base = AUTH0_API_ENDPOINT.format(domain=cfg.auth0_domain)
    response = requests.get(
        f"{api_base}/users/{user_id}",
        headers={
            "Authorization": f"Bearer {management_api_token}",
            "Content-Type": "application/json",
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def update_user_metadata(
    user_id: str,
    management_api_token: str,
    app_metadata: Optional[dict] = None,
    user_metadata: Optional[dict] = None,
    config: Optional[IdentityConfig] = None,
) -> dict:
    cfg = config or get_config()
    api_base = AUTH0_API_ENDPOINT.format(domain=cfg.auth0_domain)
    payload = {}
    if app_metadata is not None:
        payload["app_metadata"] = app_metadata
    if user_metadata is not None:
        payload["user_metadata"] = user_metadata
    response = requests.patch(
        f"{api_base}/users/{user_id}",
        json=payload,
        headers={
            "Authorization": f"Bearer {management_api_token}",
            "Content-Type": "application/json",
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def get_user_roles(
    user_id: str,
    management_api_token: str,
    config: Optional[IdentityConfig] = None,
) -> list[dict]:
    cfg = config or get_config()
    api_base = AUTH0_API_ENDPOINT.format(domain=cfg.auth0_domain)
    response = requests.get(
        f"{api_base}/users/{user_id}/roles",
        headers={
            "Authorization": f"Bearer {management_api_token}",
            "Content-Type": "application/json",
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def enrich_profile_with_roles(
    access_token: str,
    management_api_token: str,
    session_id: Optional[str] = None,
    config: Optional[IdentityConfig] = None,
) -> dict:
    cfg = config or get_config()
    raw_claims = fetch_userinfo(access_token=access_token, config=cfg)
    profile = NormalizedProfile.from_auth0_claims(raw_claims)
    roles = []
    if profile.provider_id:
        try:
            roles = get_user_roles(
                user_id=profile.sub,
                management_api_token=management_api_token,
                config=cfg,
            )
        except requests.HTTPError:
            pass
    role_names = [r.get("name", "") for r in roles] if isinstance(roles, list) else []
    profile_dict = {
        "sub": profile.sub,
        "email": profile.email,
        "email_verified": profile.email_verified,
        "name": profile.name,
        "given_name": profile.given_name,
        "family_name": profile.family_name,
        "picture": profile.picture,
        "locale": profile.locale,
        "provider": profile.provider,
        "provider_id": profile.provider_id,
        "roles": role_names,
    }
    audit_record = AuditRecord(
        event_type=AuditEventType.PROFILE_FETCHED,
        session_id=session_id,
        user_id=profile.sub,
        provider=PROVIDER,
        details={
            "email": profile.email,
            "roles": role_names,
        },
    )
    return {
        "profile": profile_dict,
        "audit_record": audit_record.to_dict(),
    }
