"""
[SAME-SCENARIO] Implements a PKCE (Proof Key for Code Exchange) login flow for public clients using Auth0.

Builds authorization URLs with PKCE code_challenge (S256 method) and exchanges
authorization codes using auth0-python SDK with code_verifier. PKCE prevents
authorization code interception attacks for SPA and native clients.

Auth0 endpoints:
  - Authorize: https://{AUTH0_DOMAIN}/authorize
  - Token:     https://{AUTH0_DOMAIN}/oauth/token

Required env vars: AUTH0_DOMAIN, AUTH0_CLIENT_ID
"""

import base64
import hashlib
import logging
import secrets
from typing import Any, Dict, Optional, Tuple

from auth0.authentication import GetToken
from auth0.authentication.users import Users

from identity_client import Auth0Config, get_state_store, get_audit_logger, load_config
from identity_models import (
    OAuthState,
    TokenResponse,
    UserProfile,
    AuditEvent,
)

logger = logging.getLogger(__name__)


class PkceState:
    """Tracks a single PKCE authorization request."""

    def __init__(
        self,
        state_value: Optional[str] = None,
        nonce: Optional[str] = None,
        code_verifier: Optional[str] = None,
    ):
        self.state = state_value or secrets.token_urlsafe(32)
        self.nonce = nonce or secrets.token_urlsafe(32)
        self.code_verifier = code_verifier or secrets.token_urlsafe(64)

    @property
    def code_challenge(self) -> str:
        """Derive S256 code challenge from verifier."""
        digest = hashlib.sha256(self.code_verifier.encode("ascii")).digest()
        return base64.urlsafe_b64encode(digest).decode("ascii").rstrip("=")


# In-memory PKCE state store
_pkce_states: Dict[str, PkceState] = {}


def store_pkce_state(state: PkceState) -> None:
    """Store a PKCE state object for later verification."""
    _pkce_states[state.state] = state


def retrieve_pkce_state(state_value: str) -> Optional[PkceState]:
    """Retrieve and remove a PKCE state object."""
    return _pkce_states.pop(state_value, None)


def build_pkce_authorization_url(
    config: Optional[Auth0Config] = None,
    redirect_uri: Optional[str] = None,
    extra_scopes: Optional[str] = None,
    connection: Optional[str] = None,
    pkce_state: Optional[PkceState] = None,
) -> Tuple[str, PkceState]:
    """
    Build an Auth0 authorization URL with PKCE S256 challenge.

    Auth0 authorize endpoint:
        https://{AUTH0_DOMAIN}/authorize?response_type=code&code_challenge=...&code_challenge_method=S256
    """
    if config is None:
        config = load_config()

    if pkce_state is None:
        pkce_state = PkceState()

    store_pkce_state(pkce_state)

    scopes = config.build_scopes()
    if extra_scopes:
        scopes = f"{scopes} {extra_scopes}"

    import urllib.parse

    params = {
        "response_type": "code",
        "client_id": config.client_id,
        "redirect_uri": redirect_uri or config.redirect_uri,
        "scope": scopes,
        "state": pkce_state.state,
        "nonce": pkce_state.nonce,
        "code_challenge": pkce_state.code_challenge,
        "code_challenge_method": "S256",
    }

    if connection:
        params["connection"] = connection

    auth_url = f"https://{config.domain}/authorize?{urllib.parse.urlencode(params)}"

    # Audit
    audit_logger = get_audit_logger()
    audit_logger.log(
        AuditEvent(
            event_type="pkce_login_start",
            provider="auth0",
            state=pkce_state.state,
            details={
                "domain": config.domain,
                "client_id": config.client_id,
                "code_challenge_method": "S256",
            },
        )
    )

    logger.info("Generated PKCE authorization URL for Auth0 (state=%s)", pkce_state.state)
    return auth_url, pkce_state


def exchange_pkce_code(
    code: str,
    state: str,
    config: Optional[Auth0Config] = None,
    redirect_uri: Optional[str] = None,
) -> TokenResponse:
    """
    Exchange an Auth0 authorization code for tokens using PKCE code_verifier.

    Uses auth0-python SDK GetToken.authorization_code() with code_verifier parameter.
    """
    if config is None:
        config = load_config()

    pkce_state = retrieve_pkce_state(state)
    if pkce_state is None:
        raise ValueError(f"Invalid or expired PKCE state: {state}")

    get_token = GetToken(config.domain, config.client_id, client_secret=None)

    token_params: Dict[str, Any] = {
        "code": code,
        "redirect_uri": redirect_uri or config.redirect_uri,
        "code_verifier": pkce_state.code_verifier,
    }

    token_data = get_token.authorization_code(**token_params)
    token_response = TokenResponse.from_provider_response(token_data)

    # Audit
    audit_logger = get_audit_logger()
    audit_logger.log(
        AuditEvent(
            event_type="pkce_token_exchange",
            provider="auth0",
            state=state,
            details={
                "domain": config.domain,
                "token_type": token_response.token_type,
                "expires_in": token_response.expires_in,
            },
        )
    )

    return token_response


def pkce_login_flow(
    redirect_uri: Optional[str] = None,
    extra_scopes: Optional[str] = None,
    connection: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Initiate a PKCE login flow. Returns authorization URL and state info.
    """
    config = load_config()
    auth_url, pkce_state = build_pkce_authorization_url(
        config=config,
        redirect_uri=redirect_uri,
        extra_scopes=extra_scopes,
        connection=connection,
    )

    return {
        "authorization_url": auth_url,
        "state": pkce_state.state,
        "code_challenge": pkce_state.code_challenge,
        "code_challenge_method": "S256",
        "provider": "auth0",
        "domain": config.domain,
    }


def pkce_callback_flow(
    code: str,
    state: str,
    redirect_uri: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Complete a PKCE login: exchange code, fetch profile, return combined result.
    """
    config = load_config()

    token_response = exchange_pkce_code(code, state, config, redirect_uri)

    # Fetch profile using the access token
    users_client = Users(config.domain, token_response.access_token)
    user_info = users_client.userinfo()
    profile = UserProfile.from_oidc_claims(user_info, provider="auth0")

    # Store token
    from identity_client import get_token_store

    token_store = get_token_store()
    token_store.store(profile.sub, token_response)

    # Audit
    audit_logger = get_audit_logger()
    audit_logger.log(
        AuditEvent(
            event_type="pkce_login_success",
            sub=profile.sub,
            email=profile.email,
            provider="auth0",
            details={
                "domain": config.domain,
            },
        )
    )

    return {
        "success": True,
        "profile": profile.to_dict(),
        "token_response": token_response.to_dict(),
        "provider": "auth0",
    }
