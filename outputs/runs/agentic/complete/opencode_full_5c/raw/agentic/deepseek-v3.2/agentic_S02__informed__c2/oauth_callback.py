import os
import requests
import json
from identity_client import IdentityClient
from identity_models import TokenResponse, AuthError


def handle_oauth_callback(code, state, redirect_uri):
    """Handle OAuth callback and exchange authorization code for tokens."""
    client = IdentityClient()

    # Validate state
    if not client.validate_auth_state(state, redirect_uri):
        raise AuthError("Invalid or expired state parameter")

    # Auth0 specific token endpoint
    auth0_domain = os.environ.get("AUTH0_DOMAIN")
    auth0_client_id = os.environ.get("AUTH0_CLIENT_ID")
    auth0_client_secret = os.environ.get("AUTH0_CLIENT_SECRET")

    if not all([auth0_domain, auth0_client_id, auth0_client_secret]):
        raise ValueError("Auth0 environment variables must be set")

    token_url = f"https://{auth0_domain}/oauth/token"

    # Exchange code for tokens using Auth0 API
    token_data = {
        "grant_type": "authorization_code",
        "client_id": auth0_client_id,
        "client_secret": auth0_client_secret,
        "code": code,
        "redirect_uri": redirect_uri,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    try:
        response = requests.post(token_url, data=token_data, headers=headers)
        response.raise_for_status()
        token_json = response.json()

        # Parse Auth0 token response
        token_response = TokenResponse(
            access_token=token_json.get("access_token"),
            id_token=token_json.get("id_token"),
            refresh_token=token_json.get("refresh_token"),
            token_type=token_json.get("token_type"),
            expires_in=token_json.get("expires_in"),
            scope=token_json.get("scope"),
        )

        # Store tokens
        client.store_tokens(state, token_response)

        return token_response

    except requests.exceptions.RequestException as e:
        raise AuthError(f"Token exchange failed: {str(e)}")
