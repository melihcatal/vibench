import os
import json
from identity_client import get_cognito_oauth_config, exchange_code_for_tokens, get_user_info
from identity_models import OAuthCallbackPayload


def handle_oauth_callback(payload: OAuthCallbackPayload, session_store: dict = None):
    config = get_cognito_oauth_config()

    if session_store and payload.state != session_store.get("state"):
        raise ValueError("State mismatch: Possible CSRF attack.")

    # Exchange authorization code for tokens
    token_response = exchange_code_for_tokens(payload.code, payload.redirect_uri, config)

    # Fetch user profile claims
    user_profile = get_user_info(token_response.access_token, config)

    return {
        "user_profile": user_profile.__dict__,
        "tokens": token_response.__dict__,
    }
