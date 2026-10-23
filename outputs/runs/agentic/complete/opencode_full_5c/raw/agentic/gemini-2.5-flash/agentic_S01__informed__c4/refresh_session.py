import requests
from identity_client import auth0_client
from identity_models import TokenRefreshRequest, AuthResponse


def refresh_session(request: TokenRefreshRequest) -> AuthResponse:
    """Refreshes an expired session or access token using Auth0 Authentication API."""
    payload = {
        "grant_type": "refresh_token",
        "client_id": auth0_client.client_id,
        "client_secret": auth0_client.client_secret,
        "refresh_token": request.refresh_token,
    }

    try:
        response = requests.post(auth0_client.authentication_url, json=payload)
        response.raise_for_status()
        data = response.json()

        return AuthResponse(
            access_token=data["access_token"],
            expires_in=data["expires_in"],
            token_type=data["token_type"],
            refresh_token=data.get("refresh_token"),  # May or may not be returned
            id_token=data.get("id_token"),
        )
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Auth0 token refresh failed: {e}")
