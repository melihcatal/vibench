import requests
import json
from dataclasses import asdict

from identity_client import FirebaseConfig
from identity_models import RefreshSessionRequest, RefreshSessionResponse

FIREBASE_REFRESH_TOKEN_URL = "https://securetoken.googleapis.com/v1/token"


def refresh_session(request: RefreshSessionRequest) -> RefreshSessionResponse:
    """
    Refreshes an expired session or access token using Firebase Authentication REST API.
    """
    if not FirebaseConfig.API_KEY:
        raise ValueError("FIREBASE_API_KEY environment variable not set.")

    params = {"key": FirebaseConfig.API_KEY}
    headers = {"Content-Type": "application/json"}
    payload = asdict(request)

    try:
        response = requests.post(
            FIREBASE_REFRESH_TOKEN_URL,
            params=params,
            headers=headers,
            data=json.dumps(payload),
        )
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()

        return RefreshSessionResponse(
            access_token=data["access_token"],
            expires_in=data["expires_in"],
            token_type=data["token_type"],
            refresh_token=data["refresh_token"],
            id_token=data["id_token"],
            user_id=data["user_id"],
            project_id=data["project_id"],
        )
    except requests.exceptions.RequestException as e:
        error_message = (
            e.response.json().get("error", {}).get("message", str(e))
            if e.response
            else str(e)
        )
        raise ValueError(f"Failed to refresh session: {error_message}")
