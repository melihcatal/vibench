from identity_client import get_auth_client
from identity_models import RefreshSessionRequest, RefreshSessionResponse
import requests
import os


def refresh_session(request: RefreshSessionRequest) -> RefreshSessionResponse:
    # Firebase Admin SDK does not directly refresh sessions or tokens.
    # This is typically handled by the Firebase Client SDK using a refresh token.
    # To simulate this, we can call Firebase's REST API for token refresh.

    api_key = os.environ.get(
        "FIREBASE_API_KEY"
    )  # You would need to set this environment variable
    if not api_key:
        raise ValueError(
            "FIREBASE_API_KEY environment variable not set. Required for token refresh simulation."
        )

    refresh_url = f"https://securetoken.googleapis.com/v1/token?key={api_key}"
    payload = {"grant_type": "refresh_token", "refresh_token": request.refresh_token}
    try:
        response = requests.post(refresh_url, json=payload)
        response.raise_for_status()
        data = response.json()

        return RefreshSessionResponse(
            id_token=data.get("id_token"),
            refresh_token=data.get(
                "refresh_token", request.refresh_token
            ),  # If new refresh token is not provided, use the old one
        )
    except requests.exceptions.RequestException as e:
        raise ValueError(
            f"Firebase token refresh failed: {e}. Check FIREBASE_API_KEY and refresh token validity."
        )
