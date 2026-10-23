"""
[SAME-SCENARIO] Fetches and normalizes federated user profile claims using Auth0.

Calls the Auth0 User Info endpoint (https://AUTH0_DOMAIN/userinfo) with the
access token obtained from token exchange, then normalizes the returned OIDC
claims into a standard UserProfile model.

Required env vars: AUTH0_DOMAIN, AUTH0_CLIENT_ID
"""

import logging
from typing import Any, Dict, Optional

from auth0.authentication.users import Users

from identity_client import Auth0Config, get_token_store, get_audit_logger, load_config
from identity_models import UserProfile, TokenResponse, AuditEvent

logger = logging.getLogger(__name__)


def fetch_user_info(
    access_token: str,
    config: Optional[Auth0Config] = None,
) -> Dict[str, Any]:
    """
    Fetch user info from the Auth0 /userinfo endpoint using the auth0-python SDK.

    Auth0 User Info endpoint:
        GET https://{AUTH0_DOMAIN}/userinfo
    """
    if config is None:
        config = load_config()

    users_client = Users(config.domain, access_token)
    user_info = users_client.userinfo()

    logger.info("Retrieved Auth0 user info for sub: %s", user_info.get("sub"))
    return user_info


def normalize_profile(
    user_info: Dict[str, Any],
    provider: str = "auth0",
) -> UserProfile:
    """
    Normalize raw Auth0 user info claims into a UserProfile model.

    Auth0 includes standard OIDC claims plus custom claims under
    namespace-based attributes. This function maps both.
    """
    profile = UserProfile.from_oidc_claims(user_info, provider=provider)

    # Auth0-specific: extract picture from user_metadata or picture
    if "picture" in user_info:
        profile.picture = user_info["picture"]

    # Auth0-specific: nickname handling
    if "nickname" in user_info:
        profile.nickname = user_info["nickname"]

    # Auth0-specific: updated_at may be a string
    if isinstance(profile.updated_at, str):
        try:
            profile.updated_at = int(float(profile.updated_at))
        except (ValueError, TypeError):
            profile.updated_at = None

    return profile


def get_profile(
    access_token: str,
    token_response: Optional[TokenResponse] = None,
    config: Optional[Auth0Config] = None,
) -> UserProfile:
    """
    Full profile fetch and normalization pipeline.

    1. Fetch user info from Auth0 /userinfo
    2. Normalize claims
    3. Store token if provided
    4. Log audit event
    """
    if config is None:
        config = load_config()

    user_info = fetch_user_info(access_token, config)
    profile = normalize_profile(user_info, provider="auth0")

    # Store token if provided
    if token_response and profile.sub:
        token_store = get_token_store()
        token_store.store(profile.sub, token_response)

    # Log the profile fetch event
    audit_logger = get_audit_logger()
    audit_logger.log(
        AuditEvent(
            event_type="profile_fetch",
            sub=profile.sub,
            email=profile.email,
            provider="auth0",
            details={
                "domain": config.domain,
                "claims_count": len(user_info),
                "email_verified": profile.email_verified,
            },
        )
    )

    logger.info(
        "Normalized Auth0 profile for sub=%s, email=%s, name=%s",
        profile.sub,
        profile.email,
        profile.name,
    )

    return profile
