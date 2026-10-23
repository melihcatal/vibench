import requests
from identity_client import Auth0Client
from identity_models import TokenRefreshRequest, AuthTokens
import logging

logging.basicConfig(level=logging.INFO)


def refresh_session(request: TokenRefreshRequest) -> AuthTokens:
    """
    Refreshes an expired session or access token using Auth0 Authentication API.
    """
    auth0_client = Auth0Client()
    token_url = auth0_client.get_auth_api_url("/oauth/token")

    payload = {
        "grant_type": request.grant_type,
        "client_id": request.client_id,
        "refresh_token": request.refresh_token,
    }
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(token_url, json=payload, headers=headers)
        response.raise_for_status()
        token_data = response.json()
        logging.info("Session refreshed successfully with Auth0.")
        return AuthTokens(
            access_token=token_data["access_token"],
            refresh_token=token_data.get("refresh_token"),
            id_token=token_data.get("id_token"),
            token_type=token_data.get("token_type"),
            expires_in=token_data.get("expires_in"),
        )
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to refresh session: {e}")
        raise
