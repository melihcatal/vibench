import requests
from identity_models import RefreshTokenRequest, RefreshTokenResponse
from identity_client import get_firebase_web_api_key


def refresh_session(request: RefreshTokenRequest) -> RefreshTokenResponse:
    api_key = get_firebase_web_api_key()
    firebase_refresh_url = f"https://securetoken.googleapis.com/v1/token?key={api_key}"

    payload = {"grant_type": "refresh_token", "refresh_token": request.refresh_token}

    try:
        response = requests.post(firebase_refresh_url, json=payload)
        response.raise_for_status()
        data = response.json()

        return RefreshTokenResponse(
            id_token=data["id_token"],
            refresh_token=data["refresh_token"],
            expires_in=data["expires_in"],
            user_id=data["user_id"],
            project_id=data["project_id"],
        )
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Firebase token refresh failed: {e}")
