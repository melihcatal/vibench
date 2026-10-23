import os
import requests
from identity_models import RefreshSessionRequest, RefreshSessionResponse

FIREBASE_WEB_API_KEY = os.getenv("FIREBASE_WEB_API_KEY")


def refresh_session(request: RefreshSessionRequest) -> RefreshSessionResponse:
    if not FIREBASE_WEB_API_KEY:
        raise ValueError("FIREBASE_WEB_API_KEY environment variable is not set.")

    rest_api_url = (
        f"https://securetoken.googleapis.com/v1/token?key={FIREBASE_WEB_API_KEY}"
    )
    headers = {"Content-Type": "application/json"}
    payload = {"grant_type": "refresh_token", "refresh_token": request.refresh_token}

    try:
        response = requests.post(rest_api_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors
        response_data = response.json()

        # The API returns 'id_token' and 'refresh_token' directly, not 'idToken' and 'refreshToken'
        # and 'expires_in' instead of 'expiresIn' in this specific endpoint.
        # Our model uses the original client-side SDK field names for consistency,
        # so we map them here.
        return RefreshSessionResponse(
            id_token=response_data["id_token"],
            refresh_token=response_data.get(
                "refresh_token", request.refresh_token
            ),  # refresh_token might not change
            expires_in=response_data["expires_in"],
        )
    except requests.exceptions.RequestException as e:
        error_message = response.json().get("error", {}).get("message", str(e))
        raise RuntimeError(f"Failed to refresh session: {error_message}")
