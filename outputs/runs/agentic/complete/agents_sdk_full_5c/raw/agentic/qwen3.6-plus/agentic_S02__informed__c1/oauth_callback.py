"""
[SAME-SCENARIO] Handles the OAuth/OIDC callback and exchanges an authorization code for tokens.

Uses the Auth0 Authentication API (https://AUTH0_DOMAIN/oauth/token) via auth0-python SDK.
Exchanges the authorization code received from the Auth0 authorize endpoint for
access, ID, and refresh tokens. Validates the state and nonce parameters.

Required env vars: AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET
"""

import logging
from typing import Any, Dict, Optional

from auth0.authentication import GetToken

from identity_client import Auth0Config, get_state_store, get_audit_logger, load_config
from identity_models import OAuthState, TokenResponse, AuditEvent

logger = logging.getLogger(__name__)


def exchange_code_for_tokens(
    code: str,
    state: str,
    nonce: Optional[str] = None,
    config: Optional[Auth0Config] = None,
    redirect_uri: Optional[str] = None,
) -> TokenResponse:
    """
    Exchange an Auth0 authorization code for tokens via the auth0-python SDK.

    Auth0 Authentication API endpoint:
        POST https://{AUTH0_DOMAIN}/oauth/token

    Required env vars: AUTH0_DOMAIN, AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET
    """
    if config is None:
        config = load_config()

    state_store = get_state_store()
    stored_state = state_store.retrieve(state)

    if stored_state is None:
        raise ValueError(
            f"Invalid or expired OAuth state: {state}. "
            "State may have already been consumed or was never issued."
        )

    # Use auth0-python SDK GetToken to exchange code
    get_token = GetToken(config.domain, config.client_id, client_secret=config.client_secret)

    token_params: Dict[str, Any] = {
        "code": code,
        "redirect_uri": redirect_uri or config.redirect_uri,
    }

    token_data = get_token.authorization_code(**token_params)

    token_response = TokenResponse.from_provider_response(token_data)

    # Log the token exchange event
    audit_logger = get_audit_logger()
    audit_logger.log(
        AuditEvent(
            event_type="token_exchange",
            provider="auth0",
            state=state,
            details={
                "domain": config.domain,
                "token_type": token_response.token_type,
                "expires_in": token_response.expires_in,
                "has_id_token": token_response.id_token is not None,
                "has_refresh_token": token_response.refresh_token is not None,
                "scope": token_response.scope,
            },
        )
    )

    logger.info(
        "Successfully exchanged Auth0 authorization code for tokens. "
        "Token type: %s, expires_in: %s",
        token_response.token_type,
        token_response.expires_in,
    )

    return token_response


def handle_callback(
    code: str,
    state: str,
    nonce: Optional[str] = None,
    redirect_uri: Optional[str] = None,
) -> Dict[str, Any]:
    """
    High-level callback handler: validates state, exchanges code, returns result.
    """
    config = load_config()

    try:
        token_response = exchange_code_for_tokens(
            code=code,
            state=state,
            nonce=nonce,
            config=config,
            redirect_uri=redirect_uri,
        )

        audit_logger = get_audit_logger()
        audit_logger.log(
            AuditEvent(
                event_type="callback_success",
                provider="auth0",
                state=state,
                details={
                    "domain": config.domain,
                    "client_id": config.client_id,
                },
            )
        )

        return {
            "success": True,
            "token_response": token_response.to_dict(),
            "provider": "auth0",
        }

    except ValueError as exc:
        audit_logger = get_audit_logger()
        audit_logger.log(
            AuditEvent(
                event_type="callback_failure",
                provider="auth0",
                state=state,
                details={"error": str(exc), "domain": config.domain},
            )
        )
        return {
            "success": False,
            "error": str(exc),
            "provider": "auth0",
        }
