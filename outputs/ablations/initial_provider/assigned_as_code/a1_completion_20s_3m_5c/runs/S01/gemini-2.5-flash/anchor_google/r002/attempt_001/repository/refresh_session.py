import os
import requests
from identity_models import RefreshSessionPayload, AuthTokens
from identity_client import get_firebase_app


def refresh_session(payload: RefreshSessionPayload) -> AuthTokens:
    # Initialize Firebase app if not already done, to ensure project_id is available
    app = get_firebase_app()
    project_id = app.project_id

    api_key = os.getenv("FIREBASE_WEB_API_KEY")
    if not api_key:
        raise ValueError("FIREBASE_WEB_API_KEY environment variable not set.")

    # Firebase Authentication REST API endpoint for token refresh
    rest_api_url = f"https://securetoken.googleapis.com/v1/token?key={api_key}"

    headers = {"Content-Type": "application/json"}
    data = {
        "grant_type": "refresh_token",
        "refresh_token": payload.refresh_token
    }

    response = requests.post(rest_api_url, json=data, headers=headers)
    response.raise_for_status()  # Raise an exception for HTTP errors

    response_data = response.json()

    # The refresh token can change after a refresh, so we return the new one.
    return AuthTokens(
        id_token=response_data["id_token"],
        refresh_token=response_data["refresh_token"],
        expires_in=int(response_data["expires_in"]),
        local_id=response_data["user_id"]  # 'user_id' is equivalent to 'localId' in this context
    )
