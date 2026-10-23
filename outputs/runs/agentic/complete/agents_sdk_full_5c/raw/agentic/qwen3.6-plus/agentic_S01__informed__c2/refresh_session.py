"""Refresh an expired session or access token using Firebase Authentication."""

import os
import requests
from identity_models import RefreshRequest, RefreshResponse


def refresh_session(request: RefreshRequest) -> RefreshResponse:
    """Refresh a Firebase ID token using the refresh token via the Firebase STS endpoint.

    Uses the Firebase Secure Token Service (securetoken.googleapis.com) to exchange
    an existing refresh token for a new ID token, access token, and updated refresh token.

    Args:
        request: RefreshRequest containing the refresh_token to exchange.

    Returns:
        RefreshResponse with new id_token, access_token, refresh_token, and expires_in.
    """
    # Firebase Secure Token Service endpoint
    token_url = "https://securetoken.googleapis.com/v1/token"

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": request.refresh_token,
    }

    response = requests.post(
        token_url,
        json=payload,
        headers={"Content-Type": "application/json"},
        timeout=30,
    )

    if response.status_code != 200:
        try:
            error_data = response.json()
            error_msg = error_data.get("error", {}).get("message", "Token refresh failed")
        except Exception:
            error_msg = f"Token refresh failed with status {response.status_code}"
        raise ValueError(f"Firebase token refresh error: {error_msg}")

    data = response.json()

    return RefreshResponse(
        id_token=data["id_token"],
        access_token=data["access_token"],
        refresh_token=data["refresh_token"],
        expires_in=int(data["expires_in"]),
        token_type=data.get("token_type", "Bearer"),
    )
