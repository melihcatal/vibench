import os
import json
import time
from typing import Dict, Any, Optional

from identity_models import OAuthConfig, TokenResponse
from identity_client import (
    get_oauth_config,
    exchange_code_for_tokens,
    generate_event_id,
    AUTH0_DOMAIN,
    AUTH0_CLIENT_ID,
)


def handle_oauth_callback(
    authorization_code: str,
    expected_state: Optional[str] = None,
    received_state: Optional[str] = None,
    code_verifier: Optional[str] = None,
    config: Optional[OAuthConfig] = None,
) -> Dict[str, Any]:
    if config is None:
        config = get_oauth_config()

    if expected_state and received_state and expected_state != received_state:
        return {
            "success": False,
            "error": "state_mismatch",
            "message": "OAuth state parameter mismatch detected",
            "provider": "auth0",
        }

    try:
        token_response = exchange_code_for_tokens(
            code=authorization_code,
            config=config,
            code_verifier=code_verifier,
        )

        audit_event = {
            "event_id": generate_event_id(),
            "event_type": "token_exchange",
            "timestamp": time.time(),
            "provider": "auth0",
            "domain": AUTH0_DOMAIN,
            "client_id": AUTH0_CLIENT_ID,
            "success": True,
            "token_type": token_response.token_type,
            "expires_in": token_response.expires_in,
            "scope": token_response.scope,
        }

        return {
            "success": True,
            "tokens": token_response.to_dict(),
            "audit_event": audit_event,
            "provider": "auth0",
        }

    except Exception as e:
        audit_event = {
            "event_id": generate_event_id(),
            "event_type": "token_exchange",
            "timestamp": time.time(),
            "provider": "auth0",
            "domain": AUTH0_DOMAIN,
            "client_id": AUTH0_CLIENT_ID,
            "success": False,
            "error": str(e),
        }

        return {
            "success": False,
            "error": "token_exchange_failed",
            "message": str(e),
            "audit_event": audit_event,
            "provider": "auth0",
        }


def validate_callback_params(
    query_params: Dict[str, str],
    expected_state: Optional[str] = None,
) -> Dict[str, Any]:
    code = query_params.get("code", "")
    state = query_params.get("state", "")
    error = query_params.get("error", "")
    error_description = query_params.get("error_description", "")

    if error:
        return {
            "valid": False,
            "error": error,
            "error_description": error_description,
            "provider": "auth0",
        }

    if not code:
        return {
            "valid": False,
            "error": "missing_code",
            "message": "Authorization code not found in callback",
            "provider": "auth0",
        }

    if expected_state and state != expected_state:
        return {
            "valid": False,
            "error": "state_mismatch",
            "message": "State parameter does not match expected value",
            "provider": "auth0",
        }

    return {
        "valid": True,
        "code": code,
        "state": state,
        "provider": "auth0",
    }


if __name__ == "__main__":
    sample_params = {"code": "sample_auth_code", "state": "sample_state"}
    validation = validate_callback_params(sample_params)
    print(json.dumps(validation, indent=2))
