from __future__ import annotations

from identity_client import load_oauth_config, fetch_userinfo
from identity_models import (
    NormalizedProfile,
    normalize_profile_claims,
    AuditEventType,
    build_audit_event,
)


def fetch_and_normalize_profile(
    access_token: str,
    provider: str = "auth0",
    connection: str | None = None,
) -> NormalizedProfile:
    config = load_oauth_config()

    raw_claims = fetch_userinfo(config, access_token)

    profile = normalize_profile_claims(
        raw_claims=raw_claims,
        provider=provider,
        connection=connection or config.connection,
    )

    audit_event = build_audit_event(
        event_type=AuditEventType.PROFILE_FETCHED,
        user_sub=profile.sub,
        client_id=config.client_id,
        connection=profile.provider_connection,
        details={
            "provider": "auth0",
            "domain": config.domain,
            "email_verified": profile.email_verified,
            "locale": profile.locale,
        },
    )

    return profile


if __name__ == "__main__":
    import sys

    if len(sys.argv) >= 2:
        profile = fetch_and_normalize_profile(sys.argv[1])
        print(f"Sub: {profile.sub}")
        print(f"Email: {profile.email}")
        print(f"Name: {profile.name}")
    else:
        print("Usage: python profile_claims.py <access_token>")
